from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from decouple import config
import random
# from django_rest_passwordreset.signals import reset_password_token_created


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens

#     """
#     token = random.randint(100000, 999999)
#     reset_password_token.key = str(token)
#     reset_password_token.save()
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'otp_code': reset_password_token.key,
#     }

#     # render email text
#     email_html_message = render_to_string('email/password_reset_email.html', context)

#     msg = EmailMessage(
#         # title:
#         subject = "Password Reset OTP for Describit",
#         # message:
#         body = email_html_message,
#         # from:
#         from_email = config('EMAIL'),
#         # to:
#         to = [reset_password_token.user.email]
#     )
#     msg.content_subtype = "html"
#     msg.send()