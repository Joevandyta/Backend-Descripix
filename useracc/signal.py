from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from decouple import config
import random
# from django_rest_passwordreset.signals import reset_password_token_created
