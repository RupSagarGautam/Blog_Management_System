from django.shortcuts import render
from .models import Partner

def about_us(request):
    partners = Partner.objects.all()
    return render(request, 'pages/aboutus.html', {'partners': partners})
