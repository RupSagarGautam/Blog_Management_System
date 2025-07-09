from django.shortcuts import render
from addBlogs import models
from django.contrib import messages
# Create your views here.

def addBlogs(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        print("Image Type: ", type(image))
        content = request.POST.get('content')
        author = request.POST.get('author')
        print(title,content,author)

        blog = models.addBlog(
            title=title,
            image=image,
            content=content,
            author=author
        )
        blog.save()
        messages.success = "Blog Added Successfully."
        
    return render(request,'pages/blogs/add-blog.html')

def blog(request):
    blogs = models.addBlog.objects.all()
    print(blogs)
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })