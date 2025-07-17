from django.shortcuts import render, redirect
from addBlogs import models
from django.contrib import messages
from addBlogs.models import addBlog, Category
from django.contrib.auth.decorators import login_required
# Create your views here.

def validate_blog(data):
    errors = {}
    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")
    image = data.get("image")
    attachment = data.get("attachment")

    if len(title) < 3 or len(title) > 50:
        errors["title"] = (
            "The title should be minimum 3 and maximum 50 characters long."
        )

    if len(content) < 10:
        errors["content"] = "The content must be minimum 10 characters long."

    if tags == "":
        errors["tags"] = "At least one tag in required"
    else:
        splitted_tags = tags.split(",")
        for tag in splitted_tags:
            if len(tag.strip()) < 2 or len(tag.strip()) > 15:
                errors["tags"] = "Tag must be at least 3 and maximum 15 character long."
            if len(splitted_tags) > 5:
                errors["tags"] = "Tag must not be more than 5. "

    if image:
        allowed_extensions = ["jpg", "png", "jpeg"]
        if image.size > 5 * 1024 * 1024:
            errors["image"] = "Image size should be less than 5MB."

        image_extension = image.name.split(".")[-1]  # splits the data by '.' and gets the last part

        if image_extension.lower() not in allowed_extensions:
            errors["image"] = (
                f"{image_extension} is not allowed, allowed extensions are .jpg, .png, .jpeg"
            )

    if attachment and attachment.size > 10 * 1024 * 1024:
        errors["attachment"] = "Attachment size should not be greater than 10 MB."

    return errors

def addBlogs(request):
    if request.method == "POST":
        data = request.POST.copy()
        data["image"] = request.FILES.get("image")
        data["attachment"] = request.FILES.get("attachment")
        errors = validate_blog(data)
        if errors:
            return render(request, "pages/blogs/add-blog.html", {"errors": errors})
        category = models.Category.objects.get( name= data['category'])
        blog = models.addBlog.objects.create(
            title=data["title"],
            content=data["content"],
            image=data["image"],
            attachment=data["attachment"],
            author = request.user,
            category = category,
        )
        
        blog.tags.add(*[tag.strip() for tag in data['tags'].split(',')])
        messages.success(request, "Blog Created Successfully!")
        return redirect("/blogs/blogs")
    
    categories = models.Category.objects.all()
    return render(request,'pages/blogs/add-blog.html', {"categories": categories})

def blog(request):
    blogs = models.addBlog.objects.all()
    print(blogs)
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })

def blogDetails(request, id):
    blog = addBlog.objects.get(id=id)
    return render( request, 'pages/blogs/blogdetails.html', {"blog": blog})

def editBlogPage(request, id):
    blog = addBlog.objects.get(id=id)
    categories = Category.objects.all()
    tags = ", ".join(blog.tags.names())
    return render(request, 'pages/blogs/editBlogPage.html', {"blog": blog, "categories": categories, 'tags': tags})

def updateBlog(request, id):
    if request.method == "POST":
        data = request.POST.copy()
        data["image"] = request.FILES.get("image")
        data["attachment"] = request.FILES.get("attachment")
        errors = validate_blog(data)
        if errors:
            categories = Category.objects.all()
            tags = data['tags']
            data['category'] = Category.objects.get(id = data['category'])
            context= {"errors": errors, "blog":data, "categories":categories, 'tags': tags}
            return render(request, "pages/blogs/editBlogPage.html", context)
        
        else:
            addBlog = addBlog.objects.get(pk=id)
            addBlog.title = data["title"]
            addBlog.content = data["content"]
            
            if data["image"]:
                addBlog.image = data["image"]
            if data["attachment"]:
                addBlog.attachment = data["attachment"]
            category = Category.objects.get( pk = data['category'] )
            addBlog.category = category
            addBlog.tags.set([tag.strip() for tag in data['tags'].split(',')])
            addBlog.save()
            messages.success(request, "Blog Updated Successfully!")
            return redirect(f'/blog/{id}')
