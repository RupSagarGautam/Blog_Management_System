from django.urls import path
from . import views

urlpatterns = [
    path('about-us/', views.about_us, name='about_us'),
    path('add-partner/', views.add_partner, name='add_partner'),
]
