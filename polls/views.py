from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Question, Choice
from django.template import loader
from django.views import generic
from django.utils import timezone
from django.contrib import messages

class IndexView(generic.ListView):
    """Display the Index view that is a list of polls question."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Display the Detail page that show all of question list."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Display the result page that show all of choice list."""

    model = Question
    template_name = 'polls/results.html'


def login(request):
    return render(request, 'polls/login.html')

def index(request):
    """Display all of Question List."""
    latest_question_list = Question.objects.order_by('-pub_date')[:]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list, }
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    """Render to the result page."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def detail(request, question_id):
    """Render to the detail page."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    """Vote function of application."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    context = {'latest_question_list': latest_question_list, }
    return HttpResponse(template.render(context, request))

def vote_for_poll(request, pk):
    """Check that polls the polls can vote or not."""
    q = Question.objects.get(pk=pk)
    if not(q.can_vote()):
        messages.error(request, "poll expires")
        return redirect('polls:index')
    return render(request, "polls/detail.html", {"question": q})
