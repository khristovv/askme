from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from questions.forms import AnswerQuestionForm
from questions.models import Question, Answer


@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # Question.objects.get(pk=question_id)
    if question.asked_to != request.user:
        return HttpResponseForbidden('Not allowed!')
    form = AnswerQuestionForm(request.POST or None)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.save()
        form.save_m2m()
        messages.success(request, 'Answer saved!')
        return redirect('inbox')
    return render(request, "questions/answer_question.html", context={"form": form, "question": question})


@ensure_csrf_cookie
@require_POST
@login_required
def toggle_like(request):
    response = {}
    user = request.user
    answer_id = request.POST.get("answer_id")
    answer = get_object_or_404(Answer, pk=answer_id)
    if answer:
        if user in answer.likes.all():
            answer.likes.remove(user)
            response["liked"] = False
        else:
            answer.likes.add(user)
            response["liked"] = True
    return JsonResponse(response)
