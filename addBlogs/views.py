from django.http import JsonResponse
from .models import Category, addBlog

# List all blogs
def blog_list(request):
    blogs = addBlog.objects.select_related("author", "category").order_by("-created_at")
    data = []
    for blog in blogs:
        data.append({
            "title": blog.title,
            "content": blog.content,
            "author": blog.author.username,
            "category": blog.category.name if blog.category else None,
            "featured": blog.featured,
            "created_at": blog.created_at,
        })
    return JsonResponse(data, safe=False)

# Show single blog
def blog_detail(request, pk):
    try:
        blog = addBlog.objects.select_related("author", "category").get(pk=pk)
        data = {
            "title": blog.title,
            "content": blog.content,
            "author": blog.author.username,
            "category": blog.category.name if blog.category else None,
            "featured": blog.featured,
            "created_at": blog.created_at,
            "updated_at": blog.updated_at,
        }
        return JsonResponse(data)
    except addBlog.DoesNotExist:
        return JsonResponse({"error": "Blog not found"}, status=404)
