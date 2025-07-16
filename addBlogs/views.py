from django.shortcuts import render, redirect, get_object_or_404
from addBlogs import models
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

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
        
        if request.user.is_staff:
            status = models.addBlog.StatusOptions.ACTIVE
        else:
            status = models.addBlog.StatusOptions.PENDING
            
        blog = models.addBlog.objects.create(
            title=data["title"],
            content=data["content"],
            image=data["image"],
            attachment=data["attachment"],
            author = request.user,
            category = category,
            status = status,
        )
        
        blog.tags.add(*[tag.strip() for tag in data['tags'].split(',')])
        messages.success(request, "Blog Created Successfully!")
        return redirect("/blogs/blogs")
    
    categories = models.Category.objects.all()
    return render(request,'pages/blogs/add-blog.html', {"categories": categories})

def editBlogPage(request, id):
    blog = models.addBlog.objects.get(id=id)
    categories = models.Category.objects.all()
    tags = ",".join(tag.name for tag in blog.tags.all())
    return render(request, 'pages/blogs/edit-blog.html', {'blog':blog, "categories": categories, "tags":tags})

def editBlog(request, id):
    blog = get_object_or_404(models.addBlog, id=id)

    if request.method == "POST":
        try:
            data = request.POST.copy()
            data['image'] = request.FILES.get('image')
            data['attachment'] = request.FILES.get('attachment')

            errors = validate_blog(data)

            if errors:
                categories = models.Category.objects.all()
                tags = data['tags']
                context = {
                    "errors": errors,
                    "blog": blog,
                    "categories": categories,
                    "tags": tags,
                }
                return render(request, 'pages/blogs/edit-blog.html', context)

            # NO ERRORS — Proceed to update
            blog.title = data["title"]
            blog.content = data["content"]

            if data.get('image'):
                blog.image = data["image"]
            if data.get('attachment'):
                blog.attachment = data["attachment"]

            # tags
            blog.tags.set([tag.strip() for tag in data['tags'].split(',') if tag.strip()])

            # category
            try:
                category = models.Category.objects.get(name=data['category'])
                blog.category = category
            except models.Category.DoesNotExist:
                messages.error(request, "Selected category does not exist.")
                return redirect(request.path)

            blog.save()
            messages.success(request, "Blog Updated Successfully!")
            return redirect(f"/blogs/{id}")

        except Exception as e:
            print("⚠️ EXCEPTION:", e)
            messages.error(request, "An error occurred during blog update.")
            return redirect(request.path)  # fallback

    # GET Request — Load the form
    categories = models.Category.objects.all()
    tags = ",".join(tag.name for tag in blog.tags.all())
    return render(request, 'pages/blogs/edit-blog.html', {
        "blog": blog,
        "categories": categories,
        "tags": tags,
    })
    
    # blog = models.addBlog.objects.get(id=id)
    # if request == "POST":
    #     data = request.POST.copy()
    #     data['image']= request.FILES.get('image')
    #     data['attachment']= request.FILES.get('attachment')
    #     errors = validate_blog(data)
    #     if errors:
    #         categories = models.Category.objects.all()
    #         tags = data['tags']
    #         context = {"errors": errors, "blog":data, "categories": categories, "tags": tags}
    #         return render(request, 'pages/blogs/edit-blog.html', context)
    #     else:
    #         blog.title = data["title"]
    #         blog.content = data["content"]
    #         if data['imgage']:
    #             blog.image = data["image"]
    #         if data['attachment']:
    #             blog.attachment = data["attachment"]
    #         blog.tags.set([tag.strip() for tag in data['tags'].split(',')])
    #         category = models.Category.objects.get(name=data['category'])
    #         blog.category = category

    #         blog.save()
    #         messages.success(request, "Blog Updated Successfully!")
    #         return redirect("/blogs/{{id}}")

def blog(request):
    blogs = models.addBlog.objects.filter(status=models.addBlog.StatusOptions.ACTIVE)
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })


def blogDetails(request, blog_id):
    blog = get_object_or_404(models.addBlog, id=blog_id)
    return render(request, 'pages/blogs/blogdetails.html', {'blog': blog})

@login_required
def my_blogs(request):
    blogs = models.addBlog.objects.filter(author=request.user)
    return render(request, 'pages/blogs/blog.html', {'blogs': blogs})
