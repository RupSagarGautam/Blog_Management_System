# This file defines the database models for the users app.
from django.db import models
from django.contrib.auth.models import User

# The Profile model extends the built-in User model with additional user information.
class profile(models.Model):
    # Gender options for the profile
    class GenderOptions(models.TextChoices):
        Male = "Male", "Male"
        Female = "Female", "Female"
        Other = "Other", "Other"
    
    # Link to the built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Optional address field
    address = models.CharField(blank=True, max_length=50, default="")
    # Optional phone number field (max 10 characters)
    phone = models.CharField(blank=True, max_length=10, default="")
    # Nationality with default value 'Nepal'
    nationality = models.CharField(blank=True, null=True, max_length=20, default="Nepal")
    # Gender field with choices from GenderOptions
    gender = models.CharField(choices=GenderOptions, default=GenderOptions.Male, max_length=6)
    # Optional profile image
    profile_image = models.ImageField(blank=True, null=True, upload_to="users")
    # Optional date of birth field
    dob = models.DateField(null=True, blank=True)
    
    def __str__(self):
      return  f"{self.user}'s Profile"
  
 