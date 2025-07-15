from django.shortcuts import render, redirect
from addBlogs import models
from django.contrib import messages
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