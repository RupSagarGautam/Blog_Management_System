from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
def loginuser(request):
    if request.method == 'POST':
        username = request.POST['Uusername']
        password = request.POST['password']
        
        check_user = User.objects.filter(username=username).exists()
        if check_user:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(username,password)
                messages.success(request,'login sucessful')
                return redirect ("home")
            else:
                messages.error(request, "Invalid username and password.")
        else:
            messages.error(request, "Username doesnt exsist.")
               
        

