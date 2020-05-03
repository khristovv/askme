from django.contrib import messages
from django.shortcuts import redirect

from questions.models import Question
from .forms import PostQuestionForm


def post_question(request, username):
    if request.user.is_authenticated and request.method == 'POST':
        form = PostQuestionForm(request.POST)
        if form.is_valid():
            q = Question(
                asked_by=request.user if not form.cleaned_data.get('is_anonymous') else None,
                asked_to=p.user,
                content=form.cleaned_data.get('question_text')
            )
            q.save()
            messages.success(request, 'Question posted successfully!')
    elif not request.user.is_authenticated:
        messages.warning(request, 'Log in to post a question.')
        redirect(request, '/login/')
