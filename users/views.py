from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from datetime import datetime
from django.contrib.auth.decorators import login_required

def loginUser(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None

        if user_obj:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect("/")
            else:
                errors['password'] = "Password does not match"
        else:
            errors['username'] = "Username does not match"

        return render(request, 'pages/login.html', {'errors': errors})
    else:
        return render(request, 'pages/login.html')


def signupUser(request):
    errors = {}
    if request.method == "POST":
        # Get form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        profile_image = request.FILES.get("profile_image")
        dob_raw = request.POST.get("dob", '').strip()
        nationality = request.POST.get("nationality")

        # Validation
        user_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        phone_exists = Profile.objects.filter(phone=phone).exists()

        if user_exists:
            errors['username'] = "Username already exists."
        if email_exists:
            errors['email'] = "Email already exists."
        if len(username) < 3:
            errors['username'] = "Username should be at least 3 characters."
        if len(first_name) < 4:
            errors['first_name'] = "First name should be at least 4 characters."
        if phone:
            if not phone.isdigit():
                errors['phone'] = "Phone number should contain only digits."
            elif len(phone) != 10:
                errors['phone'] = "Phone number should be 10 digits."
        else:
            errors['phone'] = "Phone number is required."
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        try:
            validate_password(password)
        except Exception as e:
            errors['password'] = str(e)
        try:
            validate_email(email)
        except Exception as e:
            errors['email'] = str(e)
        # DOB parsing and validation
        if dob_raw:
            try:
                dob_parsed = datetime.strptime(dob_raw, "%Y-%m-%d").date()
            except ValueError:
                errors['dob'] = 'Invalid date format. Please use YYYY-MM-DD.'
        else:
            errors['dob'] = 'Date of birth is required.'
        # If errors, return form with error messages
        if errors:
            print("Signup Errors:", errors)
            return render(request, 'pages/signup.html', {'errors': errors})
        # If all good, try saving user and profile
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Only create profile if it doesn't exist
            if not Profile.objects.filter(user=user).exists():
                profile = Profile(
                    user=user,
                    address=address,
                    phone=phone,
                    gender=gender,
                    dob=dob_parsed,
                    nationality=nationality,
                    profile_image=profile_image if profile_image else "users/default_user.png"
                )
                profile.save()
            messages.success(request, "You have successfully signed up")
            print("Signup successful, redirecting to login page")
            return redirect("/auth/log-in")
        except Exception as e:
            print("Error during signup:", e)
            errors['general'] = "Something went wrong during signup. Please try again or contact support."
            return render(request, 'pages/signup.html', {'errors': errors})
    else:
        return render(request, 'pages/signup.html')


@login_required(login_url="/auth/log-in")
def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    print("Logout Success")
    return redirect("/auth/log-in")



