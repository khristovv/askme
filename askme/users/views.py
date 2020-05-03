from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from questions.forms import PostQuestionForm
from questions.models import Question
from users.models import Profile
from .forms import UserCreationForm
from .utils import send_account_confirmation_email, account_confirmation_token_generator


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_email = form.cleaned_data.get('email')
            send_account_confirmation_email(
                user_email, {
                    'user': user,
                    'domain': get_current_site(request),
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_confirmation_token_generator.make_token(user)
                }
            )
            messages.success(request, f'An account confirmation email was sent to: {user_email}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_confirmation_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Account confirmed!')
    else:
        return HttpResponse('Confirmation token has expired or has been altered!')


def profile(request, username):
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
    return render(request, 'users/profile.html', {
        'question_max_length': 512,
        'profile': p,
        'questions': questions,
        'form': form
    })


@login_required
def like_answer(request):
    # TODO
    pass
