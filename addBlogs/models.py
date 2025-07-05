from django.db import models
from django.utils import timezone

class addBlog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'blog_images/')
    content = models.TextField()
    author = models.CharField(max_length=50, default='Anonymous')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.author}"