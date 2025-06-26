from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def loginuser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        check_user = User.objects.filter(username=username).exists()
        if check_user:
            authenticated_user = authenticate(
                request, username=username, password=password
            )
            if authenticated_user:
                login(username, password)
                messages.success(request, "login succeddfully!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
                return redirect("auth/log-in")
        else:
            messages.error(request, "user doesnot exist")