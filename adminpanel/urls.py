from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from adminpanel.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
]