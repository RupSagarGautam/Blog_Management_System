from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from addBlogs.models import addBlog
from addBlogs import models
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import *
from django.contrib import messages
from users.views import *
from users.models import Profile
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django.contrib import messages


# Client Side Views
def aboutUS(request):
    return render(request, 'pages/aboutus.html')


def blog(request):
    blogs = models.addBlog.objects.all()
    return render(request, 'pages/blogs/blog.html', { 'blogs': blogs })

def blogDetails(request, id):
    blog = get_object_or_404(addBlog, id=id)

    if blog.status in [addBlog.StatusOptions.INACTIVE, addBlog.StatusOptions.PENDING, addBlog.StatusOptions.INACTIVE]:
        if blog.author != request.user and not request.user.is_staff:
            return redirect('/blogs/blogs')

    recent_blog = addBlog.objects.filter(
        status=addBlog.StatusOptions.ACTIVE
    ).exclude(id=id).order_by('-created_at')[:4]

    return render(request, 'pages/blogs/blogdetails.html', {
        "blog": blog,
        "blogs": blog,  # for template compatibility
        "recent_blog": recent_blog,
    })
def blogListAdmin(request):
    pending_blogs = addBlog.objects.all().order_by('-created_at')
    return render(request, 'pages/bloglist.html', {'pending_blogs': pending_blogs})


def landingPage(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')

        featured_blogs = addBlog.objects.filter(
            status=addBlog.StatusOptions.ACTIVE,
            featured=True
        ).order_by('-created_at')

        recent_blogs = addBlog.objects.filter(
            status=addBlog.StatusOptions.ACTIVE
        ).order_by('-created_at')

        if query:
            featured_blogs = featured_blogs.filter(title__icontains=query)
            recent_blogs = recent_blogs.filter(title__icontains=query)

        context = {
            "featured_blogs": featured_blogs,
            "recent_blogs": recent_blogs
        }

        return render(request, 'pages/home.html', context)  
    return render(request, 'pages/index.html')

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            return render(request, 'pages/login.html', {
                'username_error': 'User with this username does not exist',
                'username_value': username
            })

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard
        else:
            return render(request, 'pages/login.html', {
                'password_error': 'Invalid password',
                'username_value': username
            })
    else:
        return render(request, 'pages/login.html')

def signupPage(request):
    return render(request, 'pages/signup.html')

def profilePage(request):
    if not request.user.is_authenticated:
        return redirect('/auth/log-in')
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/profile.html', context)

def editUserProfile(request):
    if not request.user.is_authenticated:
        return redirect('/auth/log-in')
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first-name', user.first_name)
        user.last_name = request.POST.get('last-name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.username = request.POST.get('username', user.username)
        user.save()
        # Update profile fields
        profile.address = request.POST.get('address', profile.address)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.nationality = request.POST.get('nationality', profile.nationality)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.dob = request.POST.get('dob', profile.dob)
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('/user-profile/')
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/edit_profile.html', context)

def contactUs(request):
    return render(request, 'pages/contacts.html')


# Admin Side Views
def addBlogAdmin(request):
    return render(request, 'pages/Addblog.html')

def updateBlogAdmin(request):
    return render(request, 'pages/updateblog.html')

def blogListAdmin(request):
    pending_blogs = addBlog.objects.all().order_by('-created_at')
    return render(request, 'pages/bloglist.html', {'pending_blogs': pending_blogs})

class CustomPasswordResetView(BasePasswordResetView):
    template_name = 'pages/password_reset.html'
    
    def form_valid(self, form):
        print("=== PASSWORD RESET DEBUG ===")
        print(f"Email submitted: {form.cleaned_data.get('email')}")
        print("About to send password reset email...")
        
        # Call the parent method to actually send the email
        response = super().form_valid(form)
        
        print("Password reset email sent successfully!")
        print("Redirecting to:", self.get_success_url())
        
        # Force print the email content
        from django.core.mail import get_connection
        connection = get_connection()
        if hasattr(connection, 'outbox') and connection.outbox:
            print("\n=== EMAIL CONTENT ===")
            for email in connection.outbox:
                print(f"To: {email.to}")
                print(f"Subject: {email.subject}")
                print(f"Body: {email.body}")
                print("=" * 50)
        
        return response
    
    def form_invalid(self, form):
        print("=== PASSWORD RESET FORM INVALID ===")
        print(f"Form errors: {form.errors}")
        return super().form_invalid(form)
