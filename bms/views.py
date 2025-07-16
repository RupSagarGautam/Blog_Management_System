from django.http import HttpResponse
from django.shortcuts import render
from addBlogs.models import addBlog
from addBlogs import models
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import *
from django.contrib import messages
from users.views import *
from users.models import Profile
from django.shortcuts import redirect

# Client Side Views
def aboutUS(request):
    return render(request, 'pages/aboutus.html')


def blog(request):
    blogs = models.addBlog.objects.all()
    print(blogs)
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })

def home(request):
    return render(request, 'pages/home.html')

def landingPage(request):
    if request.user.is_authenticated:
        return render(request, 'pages/home.html')
    return render(request, 'pages/index.html')

def loginPage(request):
    return render(request, 'pages/login.html')

def signupPage(request):
    return render(request, 'pages/signup.html')

def profilePage(request):
    if not request.user.is_authenticated:
        return redirect('/auth/log-in')
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/profile.html', context)

def editUserProfile(request):
    if not request.user.is_authenticated:
        return redirect('/auth/log-in')
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first-name', user.first_name)
        user.last_name = request.POST.get('last-name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.save()
        # Update profile fields
        profile.address = request.POST.get('address', profile.address)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.nationality = request.POST.get('nationality', profile.nationality)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.dob = request.POST.get('dob', profile.dob)
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('/user-profile/')
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/edit_profile.html', context)

def contactUs(request):
    return render(request, 'pages/contacts.html')

def blogDetails(request):
    return render(request, 'pages/blogdetails.html')
# Admin Side Views
def addBlogAdmin(request):
    return render(request, 'pages/Addblog.html')

def updateBlogAdmin(request):
    return render(request, 'pages/updateblog.html')

def blogListAdmin(request):
    return render(request, 'pages/bloglist.html')
