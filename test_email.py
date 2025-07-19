#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bms.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings

# Test password reset email
print("Testing password reset email...")

# Get the user
user = User.objects.get(email='rejinadangal4@gmail.com')
print(f"Found user: {user.username}")

# Create the form
form = PasswordResetForm()
form.cleaned_data = {'email': 'rejinadangal4@gmail.com'}

# Manually create the email content
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Generate the token
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))

# Create the reset URL
reset_url = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

# Create the email content
subject = "Password reset on localhost:8000"
message = f"""You're receiving this email because you requested a password reset for your user account at localhost:8000.

Please go to the following page and choose a new password:
{reset_url}

Your username, in case you've forgotten: {user.username}

Thanks for using our site!

The localhost:8000 team
"""

print("\n=== EMAIL CONTENT ===")
print(f"To: {user.email}")
print(f"Subject: {subject}")
print(f"Body:\n{message}")
print("=" * 50)
print(f"Reset URL: {reset_url}") 