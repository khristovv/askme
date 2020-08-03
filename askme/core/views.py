from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

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
    # TODO: refactor into a class based view
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        messages.warning(request, f"No user found with username: {username}")
        return HttpResponse(f"No user found with username: {username}")
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostQuestionForm(request.POST)
        if form.is_valid():
            q = Question(
                asked_by=request.user if not form.cleaned_data.get('is_anonymous') else None,
                asked_to=profile.user,
                content=form.cleaned_data.get('question_text')
            )
            q.save()
            messages.success(request, 'Question posted successfully!')
    elif request.method == 'POST' and not request.user.is_authenticated:
        messages.warning(request, 'Log in to post a question.')
        return redirect('/login/')
    form = PostQuestionForm()
    questions = profile.user.get_public_questions()
    paginator = Paginator(questions, 5)
    questions_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/board.html', {
        'question_max_length': 512,
        'profile': profile,
        'questions_page': questions_page,
        'form': form
    })


@login_required
def inbox(request):
    unanswered_questions = request.user.get_unanswered_questions()
    paginator = Paginator(unanswered_questions, 5)
    questions_page = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/inbox.html', {
        'questions_page': questions_page
    })
