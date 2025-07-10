from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        check_user = User.objects.filter(username=username).exists()
        if check_user:
            authenticated_user =  authenticate (request, username= username ,password= password)      
            if authenticated_user :
                login(username, password)
                messages.success(request, "you have successfully logged in ")
                return redirect('home')
            else:
                messages.error(request, "invalid username or password")
                return redirect('auth/log-in')
        else: 
            messages.error(request, "user doesnt exist")
            return redirect('auth/log-in')