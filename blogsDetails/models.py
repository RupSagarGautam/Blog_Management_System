# blog/models.py
from django.db import models
from django.utils import timezone
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200) # For clean URLs
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    intro_paragraph = models.TextField(help_text="A short introductory paragraph for the blog.")
    content = models.TextField() # Main content of the blog
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags (e.g., tech, webdev, python)")
    class Meta:
        ordering = ['-publish_date'] # Order by newest first
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', kwargs={'slug': self.slug})
