from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from questions.forms import AnswerQuestionForm
from questions.models import Question


@login_required
def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question.asked_to != request.user:
        return HttpResponse('Not allowed!')
    form = AnswerQuestionForm(request.POST or None)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.save()
        form.save_m2m()
        messages.success(request, 'Answer saved!')
        return redirect('inbox')
    return render(request, "questions/answer_question.html", context={"form": form, "question": question})
