from django.shortcuts import render
from addBlogs import models
# Create your views here.

def home(request):
    blogs = models.addBlog.objects.all().order_by('-id')
    return render(request, 'pages/blog.html', {'blogs': blogs})