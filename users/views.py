from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        check_user = User.objects.filter(username=username).exists()
        if check_user:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(username,password)
                messages.success(request, 'Login successful!')
                return render(request, 'home')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
                return render(request, 'login.html')
        else:
<<<<<<< HEAD
            messages.error(request, 'User does not exist. Please sign up.')
=======
            messages.error(request, 'User does not exist. Please sign up.')
            
>>>>>>> d4a4c5187dbb12f6856aea3678e98ce114aac07e
