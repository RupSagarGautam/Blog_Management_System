from django.contrib import admin
from addBlogs import models

class addBlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'created_at', 'updated_at')
    search_fields = ['title']



admin.site.register(models.addBlog, addBlogAdmin)
admin.site.register(models.Category)