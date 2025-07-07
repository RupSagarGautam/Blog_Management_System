from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gender', 'address', 'phone', 'profile_image', ]

admin.site.register(Profile, ProfileAdmin)
