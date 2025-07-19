from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from addBlogs import models

class addBlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'status',
        'created_at',
        'updated_at',
        'view_link',
        'delete_link'
    )
    list_filter = ('author', 'created_at', 'status')
    search_fields = ['title']

    def view_link(self, obj):
        url = f'/blogs/{obj.id}'  # Public view URL
        return format_html(
            '<a href="{}" target="_blank" title="View Blog">'
            '<i class="fa-solid fa-eye" style="color: #007bff;"></i></a>',
            url
        )
    view_link.short_description = 'View Blog'

    def delete_link(self, obj):
        url = reverse('admin:addBlogs_addblog_delete', args=[obj.pk])  # Admin delete URL
        return format_html(
            '<a style="color: red !important; background:none !important;" href="{}">Delete</a>',
            url
        )
    delete_link.short_description = 'Delete Blog'

admin.site.register(models.addBlog, addBlogAdmin)
admin.site.register(models.Category)
