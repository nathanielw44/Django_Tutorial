from django.shortcuts import render, get_object_or_404, get_list_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)  # (the request, template, data to pass)
#
#
# def detail(request, qid):
#     question = get_object_or_404(Question, pk=qid)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, qid):
#     question = get_object_or_404(Question, pk=qid)
#
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, qid):
    question = get_object_or_404(Question, pk=qid)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])  # access the POST request data
    except (KeyError, Choice.DoesNotExist):
        # just render the same detail view again if post fails
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1  # update the choice's vote field
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
