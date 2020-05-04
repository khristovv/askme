from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from questions.forms import PostQuestionForm
from questions.models import Question
from users.models import Profile


def home(request):
    if request.user.is_authenticated:
        return redirect(
            'board',  # a view name
            username=request.user.username)
    return render(request, 'core/home.html')


def board(request, username):
    try:
        p = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        messages.warning(request, f"No user found with username: {username}")
        return HttpResponse(f"No user found with username: {username}")
    if request.method == 'POST' and request.user.is_authenticated:
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
        redirect('/login/')
    form = PostQuestionForm()
    questions = p.user.get_answered_questions()
    return render(request, 'core/board.html', {
        'question_max_length': 512,
        'profile': p,
        'questions': questions,
        'form': form
    })

