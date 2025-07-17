from django.db import models

# Create your models here.
class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='partner_logos/')
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, default="Kathmandu")

    def __str__(self):
        return self.name
