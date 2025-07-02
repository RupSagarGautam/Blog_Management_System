from django.contrib import admin
from .models import profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','gender', 'address','phone','profile_image']

admin.site.register(profile, ProfileAdmin )