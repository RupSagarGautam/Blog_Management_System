from django.urls import path
from . import views

urlpatterns = [
    path("signup-user/", views.signupUser, name="signup-user"),
    path("sign-up/", views.signupUser, name="sign-up"),
    path("log-in/", views.loginUser, name="login-user"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("signup-user/", views.signupUser, name="signup-user"),
    path("sign-up/", views.signupUser, name="sign-up"),
    path("log-in/", views.loginUser, name="login-user"),
]
