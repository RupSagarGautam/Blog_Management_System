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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from bms import views
from users import views as user_views

# Serve static files during development
auth_urlpatterns = [
    path('log-in/', user_views.loginUser, name='login'),
    path('sign-up/', user_views.signupUser),
    path('logout/', user_views.logoutUser)
]

# Static files (CSS, JavaScript, Images)
blog_urlpatterns = [
    path('add-blog/', views.addBlogs, name='addBlog'),
    path('add-blog/', views.addBlog),
    path('blogs/', views.blog),
    path('blog-details/', views.blogDetails),  
] 

urlpatterns = [
    
    path('',views.landingPage),
    path('admin/', admin.site.urls),
    path('home/', views.home),
    
    path('sign-up/',views.signupPage),
    path('user-profile/',views.profilePage),
    path('contact-us/',views.contactUs),
    path('blog-details', views.blogDetails),
    path('add-blog-admin/',views.addBlogAdmin),
    path('update-blog-admin/',views.updateBlogAdmin),
    path('view-blog-list/',views.blogListAdmin),
    
    path('user-profile/', views.profilePage),
    
    path('auth/', include(auth_urlpatterns)),
    path('blogs/', include(blog_urlpatterns)),

    path('about-us/', include('about.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
