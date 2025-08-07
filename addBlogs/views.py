from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from addBlogs import models
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def validate_blog(data):
    errors = {}
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    tags = data.get("tags", "").strip()
    image = data.get("image")
    attachment = data.get("attachment")

    # Title
    if not title or len(title) < 3 or len(title) > 50:
        errors["title"] = "The title should be between 3 and 50 characters long."

    # Content
    if not content or len(content) < 10:
        errors["content"] = "The content must be at least 10 characters long."

    # Tags
    if not tags:
        errors["tags"] = "At least one tag is required."
    else:
        splitted_tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if len(splitted_tags) > 5:
            errors["tags"] = "Tags must not be more than 5."
        for tag in splitted_tags:
            if len(tag) < 2 or len(tag) > 15:
                errors["tags"] = "Each tag must be between 2 and 15 characters long."
                break

    # Image
    if image:
        allowed_extensions = ["jpg", "jpeg", "png"]
        image_extension = image.name.split(".")[-1].lower()
        if image.size > 5 * 1024 * 1024:
            errors["image"] = "Image size should be less than 5MB."
        elif image_extension not in allowed_extensions:
            errors["image"] = f"Invalid file type '{image_extension}'. Allowed: jpg, jpeg, png."
    else:
        addBlogs.image = image
        if image == None:
            errors["image"] = "An Image is required"

    # Attachment (optional)
    if attachment and attachment.size > 10 * 1024 * 1024:
        errors["attachment"] = "Attachment size should not exceed 10MB."

    return errors


def addBlogs(request):
    categories = models.Category.objects.all()  # define early to avoid UnboundLocalError

    if request.method == "POST":
        data = request.POST.copy()
        data["image"] = request.FILES.get("image")
        data["attachment"] = request.FILES.get("attachment")

        errors = validate_blog(data)

        # Category validation
        try:
            category = models.Category.objects.get(name=data.get("category"))
        except models.Category.DoesNotExist:
            errors["category"] = "Selected category does not exist."

        if errors:
            return render(request, "pages/blogs/add-blog.html", {
                "errors": errors,
                "categories": categories,
                "data": data  # to repopulate form inputs if needed
            })

        status = models.addBlog.StatusOptions.ACTIVE if request.user.is_staff else models.addBlog.StatusOptions.PENDING
        is_featured = request.POST.get("featured") == "on"

        blog = models.addBlog.objects.create(
            title=data["title"],
            content=data["content"],
            image=data["image"],
            attachment=data["attachment"],
            author=request.user,
            category=category,
            status=status,
            featured=is_featured
        )

        blog.tags.add(*[tag.strip() for tag in data["tags"].split(",") if tag.strip()])
        messages.success(request, "Blog Created Successfully!")
        return redirect("/blogs/blogs")

    return render(request, 'pages/blogs/add-blog.html', {"categories": categories, "errors": {}})

def editBlogPage(request, id):
    blog = models.addBlog.objects.get(id=id)
    categories = models.Category.objects.all()
    tags = ",".join(tag.name for tag in blog.tags.all())
    return render(request, 'pages/blogs/edit-blog.html', {'blog':blog, "categories": categories, "tags":tags})

def editBlog(request, id):
    blog = get_object_or_404(models.addBlog, id=id)
    categories = models.Category.objects.all()
    tags = ",".join(tag.name for tag in blog.tags.all())
    errors = {}

    # Access Control Check
    if not (blog.author == request.user or request.user.is_staff):
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect("/blogs/blogs")

    if request.method == "POST":
        data = request.POST.copy()
        if data['image']:
            data['image'] = request.FILES.get('image')
        data['attachment'] = request.FILES.get('attachment')
        errors = validate_blog(data)

        # Category existence validation
        try:
            category = models.Category.objects.get(name=data['category'])
        except models.Category.DoesNotExist:
            errors["category"] = "Selected category does not exist."

        if errors:
            return render(request, 'pages/blogs/edit-blog.html', {
                "errors": errors,
                "blog": blog,
                "categories": categories,
                "tags": data['tags'],
            })
        else:
            # Update blog fields
            blog.title = data["title"]
            blog.content = data["content"]
            blog.category = category
            blog.status = models.addBlog.StatusOptions.ACTIVE if request.user.is_staff else models.addBlog.StatusOptions.PENDING

            if data.get("image"):
                blog.image = data["image"]
            if data.get("attachment"):
                blog.attachment = data["attachment"]

            blog.tags.set([tag.strip() for tag in data['tags'].split(',') if tag.strip()])
            blog.save()

            messages.success(request, "Blog Updated Successfully!")
            return redirect(f"/blogs/{id}")

    # GET Request
    return render(request, 'pages/blogs/edit-blog.html', {
        "blog": blog,
        "categories": categories,
        "tags": tags,
        "errors": errors,
    })

def blogs(request):
    categories = models.Category.objects.all()

    blogs = models.addBlog.objects.filter(
        status=models.addBlog.StatusOptions.ACTIVE
    ).order_by('-created_at')

    category_id = request.GET.get('category')
    query = request.GET.get('q')  # for search
    current_category = None

    if category_id:
        blogs = blogs.filter(category__id=category_id)
        current_category = categories.filter(id=category_id).first()

    if query:
        blogs = blogs.filter(title__icontains=query)

    context = {
        'categories': categories,
        'blogs': blogs,
        'current_category': current_category,
        'query': query or '',  # so it keeps input value in the form
    }
    return render(request, 'pages/blogs/blog.html', context)


def blogDetails(request, blog_id):
    blog = get_object_or_404(models.addBlog, id=blog_id)
    blog = blog.filter(status=models.addBlog.StatusOptions.ACTIVE)
    if models.addBlog.status == models.addBlog.StatusOptions.INACTIVE or models.addBlog.status == models.addBlog.StatusOptions.PENDING:
        return redirect('/blogs/blogs')
    return render(request, 'pages/blogs/blogdetails.html', {'blog': blog})

@login_required
def my_blogs(request):
    blogs = models.addBlog.objects.filter(author=request.user)
    return render(request, 'pages/blogs/blog.html', {'blogs': blogs})

def home(request, category_id=None):
    categories = models.Category.objects.all()
    query = request.GET.get('q')

    # Start with all active blogs
    featured_blogs = models.addBlog.objects.filter(
        status=models.addBlog.StatusOptions.ACTIVE,
        featured=True
    ).order_by('-created_at')

    recent_blogs = models.addBlog.objects.filter(
        status=models.addBlog.StatusOptions.ACTIVE
    ).order_by('-created_at')

    # Filter by query if present
    if query:
        featured_blogs = featured_blogs.filter(title__icontains=query)
        recent_blogs = recent_blogs.filter(title__icontains=query)

    # Filter by category if category_id is present
    if category_id:
        featured_blogs = featured_blogs.filter(category__id=category_id)
        recent_blogs = recent_blogs.filter(category__id=category_id)

    context = {
        'categories': categories,
        "featured_blogs": featured_blogs,
        "recent_blogs": recent_blogs
    }

    return render(request, 'pages/home.html', context)

def blogs_by_category(request, category_id=None):
    categories = models.Category.objects.all()
    blogs = models.addBlog.objects.filter(
        status=models.addBlog.StatusOptions.ACTIVE
    ).order_by('-created_at')

    current_category = None
    if category_id:
        blogs = blogs.filter(category__id=category_id)
        # Get category object for displaying name
        current_category = categories.filter(id=category_id).first()

    context = {
        'categories': categories,
        'blogs': blogs,
        'current_category': current_category,
    }
    return render(request, 'blogs/blogs.html', context)

def blog_list(request):
    query = request.GET.get('q')
    if query:
        blogs = models.addBlog.objects.filter(title__icontains=query, status='APPROVED')  # adjust status filter as needed
    else:
        blogs = models.addBlog.objects.filter(status='APPROVED')

    context = {'blogs': blogs}
    return render(request, 'pages/blogs/blog.html', context)

def deleteblog(request, blog_id):
    if request.method == "POST":
        blog = get_object_or_404(models.addBlog, id=blog_id)

        # Optional: Check if request.user is the author/admin
        if request.user == blog.author or request.user.is_superuser:
            blog.delete()
            messages.success(request, "Blog deleted successfully.")
        else:
            messages.error(request, "You are not authorized to delete this blog.")
        return redirect('/blogs/blogs')  
    else:
        messages.error(request, "Invalid request method.")
        return redirect('/blogs/blogs')