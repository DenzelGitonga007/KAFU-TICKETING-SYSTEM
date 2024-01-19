from django.contrib import admin

# Register your models here.
from .models import Ticket

# Manage the Ticket model
class TicketAdmin(admin.ModelAdmin):
    """Manage the ticket details"""
    list_display = ['ticket_number', 'user']
    search_fields = ['ticket_number', 'user']

# Register the admin model
admin.site.register(Ticket, TicketAdmin)
