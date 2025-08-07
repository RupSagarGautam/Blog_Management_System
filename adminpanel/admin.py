from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from addBlogs.models import addBlog  # your blog model
from django.db.models.functions import TruncMonth
from django.db.models import Count
import datetime

class CustomAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name="custom_dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Total counts
        total_users = User.objects.count()
        total_blogs = addBlog.objects.count()

        # Monthly blog counts (last 6 months)
        six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
        monthly_counts = (
            addBlog.objects
            .filter(created_at__gte=six_months_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        return TemplateResponse(request, "admin/custom_dashboard.html", {
            "total_users": total_users,
            "total_blogs": total_blogs,
            "monthly_counts": monthly_counts,
        })

# Replace default admin site
admin_site = CustomAdminSite(name='custom_admin')
admin.site = admin_site

