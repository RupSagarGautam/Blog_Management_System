from django.contrib import admin
from .models import Partner, TeamMember

# Register your models here.

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'location']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']
    search_fields = ('name', 'description', 'image')
    