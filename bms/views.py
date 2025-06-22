from django.http import HttpResponse
from django.shortcuts import render

# Client Side Views
def aboutUS(request):
    return render(request, 'aboutus.html')

def addBlogUser(request):
    return render(request,'add-blog.html')

def blog(request):
    return render(request, 'blog.html')

def home(request):
    return render(request, 'home.html')

def landingPage(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

# Admin Side Views
def addBlogAdmin(request):
    return render(request, 'Addblog.html')

def updateBlogAdmin(request):
    return render(request, 'updateblog.html')

def blogListAdmin(request):
    return render(request, 'blog-list.html')
