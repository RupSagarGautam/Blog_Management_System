"""
URL configuration for bms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bms import views

urlpatterns = [
    
    path('',views.landingPage),
    path('admin/', admin.site.urls),
    path('about-us/',views.aboutUS ),
    path('add-blog/', views.addBlogUser),
    path('blogs/', views.blog),
    path('home/', views.home),
    path('log-in/',views.login),
    path('sign-up/',views.signup),
    path('add-blog-admin/',views.addBlogAdmin),
    path('update-blog-admin/',views.updateBlogAdmin),
    path('view-blog-list/',views.blogListAdmin)
]
