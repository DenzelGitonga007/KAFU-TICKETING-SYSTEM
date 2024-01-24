from django.contrib import admin

# Register your models here.
from .models import Issue

# Manage the Ticket model
class IssueAdmin(admin.ModelAdmin):
    """Manage the ticket details"""
    list_display = ['ticket_number', 'user']
    search_fields = ['ticket_number', 'user']

# Register the admin model
admin.site.register(Issue, IssueAdmin)
