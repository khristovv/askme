from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

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


@login_required
def profile(request):
    return render(request, 'users/profile.html')
