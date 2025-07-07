
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.views import User

class addBlog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to= 'blog_images/')
    content = models.TextField()
    author = models.CharField(max_length=50, default='Anoynymous')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.author}"