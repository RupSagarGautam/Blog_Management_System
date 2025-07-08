from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile #model exists in same folder
from django.contrib.auth.password_validation import validate_password #password validation automatically done by django
from django.core.validators import validate_email #email validation automatically done by django
from datetime import datetime
from django.contrib.auth.decorators import login_required



def loginUser(request):
    errors = {}
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Check if user with given email exists
        # try:
        user_obj = User.objects.get(username=username) #fetches user object with given username
        #     username = user_obj.username
        # except User.DoesNotExist:
        #     user_obj = None
        #     username = None
        
        if user_obj:
            # Authenticate using username and password
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user) # saves the user data in session 
                messages.success(request, "You have successfully logged in")
                return redirect("/") # redirects to /home route
            else:
                errors['password'] = "Invalid Password!" #stores error in key 'password'
        else:
            errors['email'] = "User with this email does not exist."
        
        if errors:
            return render(request, 'pages/login.html', {'errors': errors}) # renders login.html with errors
    else:
        return render(request, 'pages/login.html')
        
def signupUser(request):
    errors = {}
    if request.method == "POST":
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
        dob = request.POST.get("dob")
        nationality = request.POST.get("nationality")
        
        user_exists = User.objects.filter(username = username).exists()
        email_exists = User.objects.filter(email = email).exists()
        phone_exists = Profile.objects.filter(phone = phone).exists()
        
        if user_exists:
            errors['username']= "Username already exists."
            
        if len(username) < 4:
            errors['username'] = "Username should be at least 4 characters."
            
        if len(first_name) < 4:
            errors['first_name'] = "First name should be at least 4 characters."
            
        if phone and not phone.isdigit():
            errors['phone'] = "Phone number should contain only digits."
            
        # if not phone:
        #     errors['phone'] = "Phone number is required."
        # elif phone_exists:
        #     errors['phone'] = "Phone number already exists."
        # elif len(phone) != 10:
        #     errors['phone'] = "Phone number should be 10 digits."

            
        # if len(password)< 6:
        #     errors['password'] = "Password should be at least 6 characters."
            
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
            
        try:
            validate_password(password)
        except Exception as e:
            errors['password'] = e
            
        try:
            if email_exists:
                errors['email'] = ["Email already exists."]
            validate_email(email)
        except Exception as e:
            errors['email'] = e
            
        dob_raw = request.POST.get('dob', '').strip()

        # Validate dob
        if dob_raw:
            try:
                dob_parsed = datetime.strptime(dob_raw, "%Y-%m-%d").date()
            except ValueError:
                errors['dob'] = 'Invalid date format. Please use YYYY-MM-DD.'
                # render form with errors...
                return render(request, 'pages/auth/signup.html', {'errors': errors})
        else:
            errors['dob'] = 'Date of birth is required.'
            return render(request, 'pages/auth/signup.html', {'errors': errors})
                
        if errors:
            print(errors)
            return render(request, 'pages/auth/signup.html', {'errors': errors})
        else:
            #creating new user in model
            user= User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            
            #creating new profile in modle for user
            # Profile.objects.create(user=user, address=address, phone=phone, gender=gender, dob=dob, nationality=nationality, profile_image=profile_image)
        
            
            #alternative method
            # user = user(username=username, email=email, first_name=first_name, last_name=last_name)
            # user.set_password(password)
            # user.save()
            
            profile = Profile(user=user, address=address, phone=phone, gender=gender,dob=dob, nationality=nationality, profile_image=profile_image)
            if profile_image:
                profile.profile_image = profile_image
            else:
                profile.profile_image = "default.jpg"
            profile.save()
            
        messages.success(request, "You have successfully signed up")
        return redirect("/auth/log-in")
    else:
        return render(request, 'pages/auth/signup.html')
    
@login_required(login_url="/auth/log-in/")    
def logoutUser(request):
    logout(request)
    messages.success(request, "You Have Successfully Log Out")
    print("Logout Success")
    return redirect("/auth/log-in")