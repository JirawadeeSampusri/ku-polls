from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import Question, Choice,Vote

import logging

from django.db.migrations import loader



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


# def index(request):
#     """Display all of Question List."""
#     latest_question_list = Question.objects.order_by('-pub_date')[:]
#     template = loader.get_template('polls/index.html')
#     context = {'latest_question_list': latest_question_list, }
#     return HttpResponse(template.render(context, request))

def results(request, question_id):
    """Render to the result page."""
    question = get_object_or_404(Question, pk=question_id)
    user_exist = Vote.objects.filter(question_id=question_id, user_id= request.user.id).exists()
    return render(request, 'polls/results.html', {'question': question, 'user_exist': user_exist})

def detail(request, question_id):
    """Render to the detail page."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
@login_required
def vote(request, question_id):
    """Vote function for polls app."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        configure()
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        configure()

        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if Vote.objects.filter(question_id=question_id, user_id=request.user.id).exists():
            configure()
            user_vote = question.vote_set.get(user=request.user)
            user_vote.choice = selected_choice
            user_vote.choice.votes += 1
            user_vote.choice.save()
            user_vote.save()
        else:
            configure()
            selected_choice.vote_set.create(user=request.user, question=question)

        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

def vote_for_poll(request, pk):
    """Check that polls the polls can vote or not."""
    q = Question.objects.get(pk=pk)
    if not(q.can_vote()):
        messages.error(request, "poll expires")
        return redirect('polls:index')
    return render(request, "polls/detail.html", {"question": q})

def show_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    user_vote = Vote.objects.filter(question_id=pk, user_id=request.user.id)
    user_exist = Vote.objects.filter(question_id=pk, user_id=request.user.id).exists()

def configure():
    """Configure loggers and log handlers"""
    filehandler = logging.FileHandler("demo.log")
    filehandler.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    filehandler.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(filehandler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(levelname)-8s %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)