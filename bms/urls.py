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
from addBlogs import views as blog_views
from users import views as user_views
from django.contrib.auth import views as auth_views


# Serve static files during development
auth_urlpatterns = [
    path('log-in/', views.loginPage, name='login'),
    path('sign-up/', user_views.signupUser),
    path('logout/', user_views.logoutUser)
]

# Static files (CSS, JavaScript, Images)
blog_urlpatterns = [
    path('add-blog/', blog_views.addBlogs, name='addBlog'),
    path('view-blogs/', blog_views.my_blogs, name='viewBlogs'),
    path('blogs/', blog_views.blogs, name='blogs'),
    path('blogs/', blog_views.blogs_by_category, name='all_blogs'),
    path('<int:id>', views.blogDetails),  
    path('<int:id>/edit-blog/', blog_views.editBlogPage, name='edit_blogPage'),
    path('<int:id>/edit/', blog_views.editBlog, name='edit_blog'),
    path('category/<int:category_id>/', blog_views.home, name='category_filter'),
    path('blogs/category/<int:category_id>/', blog_views.blogs_by_category, name='blogs_by_category'),
] 

urlpatterns = [
    
    path('',views.landingPage),
    path('',blog_views.home, name='home'),
    path('admin/', admin.site.urls),
    
    path('sign-up/',views.signupPage),
    path('user-profile/',views.profilePage),
    path('contact-us/',views.contactUs),
    path('add-blog-admin/',views.addBlogAdmin),
    path('update-blog-admin/',views.updateBlogAdmin),
    path('view-blog-list/',views.blogListAdmin),
    path('user-profile/', views.profilePage),
    path("edit-user", views.editUserProfile),
    
    path('auth/', include(auth_urlpatterns)),
    path('blogs/', include(blog_urlpatterns)),
    path('about-us/', include('about.urls')),

    # django-allauth urls
    path('accounts/', include('allauth.urls')),
     path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pages/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pages/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pages/password_reset_complete.html'
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

    
    