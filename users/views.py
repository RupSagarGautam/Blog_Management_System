from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from users.models import profile
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email





def loginUser(request):
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        
        # returns boolean value if any value matching username exists in model User
        check_user = User.objects.filter(username=username).exists() 
        if check_user:
            # for authenticating user with username and password
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user) # saves the user data in session 
                messages.success(request, "You have successfully logged in")
                return redirect("/") # redirects to /home route
            else:
                errors['password'] = "Invalid Password!" #stores error in key 'password'
        else:
            errors['username'] = "User doesnot exist."
        
        if errors:
            return render(request, 'pages/auth/login.html', {'errors': errors}) # renders login.html with errors
        
        
        
        
def signupUser(request):
    
    errors= {}
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
        user_exists = User.objects.filter(username= username).exists()
        email_exists=User.objects.filter(email=email).exists()
        phone_exists = profile.objects.filter(phone=phone).exists()
        
        if user_exists:
            errors['username']= "username already exists."       

        if phone_exists:   
            errors['phone']= "phone number already exists."  
            
        if len(phone) != 10:
            errors['phone'] = "Iphone number should be 10 digits!"
            
        if len(password)<6:
            errors['password'] = "Password should be at least 6 characters long!"
            
        if password !=confirm_password:
            errors['confirm_password'] = "Passwords do not match!"
            
        if len (first_name)<3:
            errors['first_name'] = "First name should be at least 3 characters long!"
            
        if len(username)<3:
            errors['username'] = "Username should be at least 3 characters long!"
            
        try:
            validate_password(password)
        except Exception as e:
            errors ['password']= str(e)
               
        try: 
            if email_exists:   
               raise Exception ("email already exists.")  
            validate_email(email)
        except Exception as e:
            errors['email'] = str(e) 
            
        if errors:
            print(errors)  # Debug: See what errors are being generated
            return render(request, 'pages/auth/signup.html', {'errors': errors})
        
         #creating a new user     
        user=User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        profile_obj = profile(user=user, address=address, phone=phone, gender=gender, dob=dob, nationality=nationality, profile_image=profile_image)
        profile_obj.save()
        
        #alternative method
        # user = User(username=username, email=email,  first_name=first_name, last_name=last_name)
        # user.set_password(password)
        # user.save()
        
    #profile = Profile(user = user, address=address, phone=phone, gender=gender, dob=dob, nationality=nationality)
    #if profile_image:
    # profile.profile_image = profile_image
    #else:
    #profile.profile_image= 'default.jpg'
    # profile.save()
    messages.success(request, "You have successfully signed up")
    return redirect('/auth/log-in')
