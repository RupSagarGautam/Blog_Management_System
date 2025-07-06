from django.db import models
from django.contrib.auth.models import User

# Creating models here.
class Profile(models.Model):
    def generateImagePath(instance, filename):
        return f'users/{instance.user.username}/{filename}'
    
    class GenderOptions(models.TextChoices):
        Male = 'Male', 'Male'
        Female = 'Female', 'Female'
        Other = 'Other', 'Other'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True, max_length=50)
    phone = models.CharField(blank= True, null= True, max_length=10)
    nationality = models.CharField(blank= True, null= True, max_length=15, default ='Nepal')
    gender = models.CharField(choices=GenderOptions.choices, default=GenderOptions.Male, max_length=6)
    profile_image = models.ImageField(upload_to='generateImagePath', blank=True, null=True, default= "users/profpic.jpg")
    dob = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user}'s Profile"

    
    
    

