from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question

# Each view must either return an HttpResponse 
# or raise an appropriate exception (404, for example)
# Anything else that they do (query the model, for example) is up to you!


# These 3 are the initial implementations. We've changed them to be generic
# class based views instead
# def index(request):
#     # uses the index template at app\templates\app\index.html
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = { 'latest_question_list':latest_question_list }
#     return render(request, 'app/index.html', context)

# def detail(request, question_id):
#     # for this we could also use the get_object_or_404() function, but this 
#     # shows the control flow for exceptions a little better
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("No such question exists")
#     return render(request, 'app/detail.html', {'question': question})

# def results(request, question_id):
#     return HttpResponse('You\'re looking at the results for question %s' % question_id)

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'app/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'app/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))