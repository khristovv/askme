from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class AccountConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_confirmation_token_generator = AccountConfirmationTokenGenerator()


def send_account_confirmation_email(user_email, context):
    # python -m smtpd -n -c DebuggingServer localhost:1025
    subject = 'Account Confirmation'
    message = render_to_string('users/account_confirmation.html', context)
    email = EmailMessage(subject, message, to=[user_email])
    email.send()


