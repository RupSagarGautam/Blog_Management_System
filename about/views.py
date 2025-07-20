from django.shortcuts import render, redirect
from about import models
from .models import TeamMember


def about_us(request):
    partners = models.Partner.objects.all()
    team = TeamMember.objects.all()
    return render(request, 'pages/aboutus.html', {'partners': partners, 'team': team})

def add_partner(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        description = request.POST.get("description")
        website = request.POST.get("website")
        logo = request.FILES.get("logo")

        models.Partner.objects.create(
            name=name,
            location=location,
            description=description,
            website=website,
            logo=logo
        )
        return redirect('aboutus')

    return render(request, 'pages/add-partner.html')
