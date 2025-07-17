from django.http import HttpResponse
from django.shortcuts import render
from addBlogs.models import addBlog, Category
from addBlogs import models
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404


# Client Side Views
def aboutUS(request):
    return render(request, 'pages/aboutus.html')


def blog(request):
    blogs = models.addBlog.objects.filter(status='Active').order_by('-created_at')
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })


def blogDetails(request, id):
    blog = addBlog.objects.get(id=id)
    return render( request, 'pages/blogs/blogdetails.html', {"blog": blog})

def editBlogPage(request, id):
    blog = addBlog.objects.get(id=id)
    categories = Category.objects.all()
    tags = ", ".join(blog.tags.names())
    return render(request, 'pages/blogs/editBlogPage.html', {"blog": blog, "categories": categories, 'tags': tags})

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
    return render(request, 'pages/profile.html')

def contactUs(request):
    return render(request, 'pages/contacts.html')

# Admin Side Views
def addBlogAdmin(request):
    return render(request, 'pages/Addblog.html')

def updateBlogAdmin(request):
    return render(request, 'pages/updateblog.html')

def blogListAdmin(request):
    return render(request, 'pages/bloglist.html')

            