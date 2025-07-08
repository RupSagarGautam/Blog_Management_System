from django.shortcuts import render, redirect
from .models import Partner

def about_us(request):
    partners = Partner.objects.all()
    return render(request, 'pages/about_us.html', {'partners': partners})

def add_partner(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        description = request.POST.get("description")
        website = request.POST.get("website")
        logo = request.FILES.get("logo")

        Partner.objects.create(
            name=name,
            location=location,
            description=description,
            website=website,
            logo=logo
        )
        return redirect('about_us')

    return render(request, 'pages/add_partner.html')
