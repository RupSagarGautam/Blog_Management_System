from django.http import HttpResponse
from django.shortcuts import render

from addBlogs import models

# Client Side Views
def aboutUS(request):
    return render(request, 'pages/aboutus.html')

def addBlogUser(request):
    return render(request,'pages/add-blog.html')

def blog(request):
    blogs = models.addBlog.objects.all()
    print(blogs)
    return render(request, 'pages/blog.html', { 'blogs': blogs })

def home(request):
    return render(request, 'pages/home.html')

def landingPage(request):
    return render(request, 'pages/index.html')

def loginPage(request):
    return render(request, 'pages/login.html')

def signupPage(request):
    return render(request, 'pages/signup.html')

def profilePage(request):
    return render(request, 'pages/profile.html')

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
