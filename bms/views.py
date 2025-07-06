from django.http import HttpResponse
from django.shortcuts import render

# Client Side Views
def aboutUS(request):
    return render(request, 'pages/auth/aboutus.html')

def addBlogUser(request):
    return render(request,'pages/auth/add-blog.html')

def blog(request):
    return render(request, 'pages/auth/blog.html')

def home(request):
    return render(request, 'pages/auth/home.html')

def landingPage(request):
    return render(request, 'pages/auth/index.html')

def loginPage(request):
    return render(request, 'pages/auth/login.html')

def signupPage(request):
    return render(request, 'pages/auth/signup.html')

def profilePage(request):
    return render(request, 'pages/auth/profile.html')

def contactUs(request):
    return render(request, 'pages/auth/contacts.html')
# Admin Side Views
def addBlogAdmin(request):
    return render(request, 'pages/auth/Addblog.html')

def updateBlogAdmin(request):
    return render(request, 'pages/auth/updateblog.html')

def blogListAdmin(request):
    return render(request, 'pages/auth/bloglist.html')



