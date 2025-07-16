from django.contrib import admin
from addBlogs import models

class addBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'created_at', 'updated_at')

admin.site.register(models.addBlog, addBlogAdmin)
    