from django.contrib import admin

# Register your models here.
from .models import Assignment

# Assignment admin
class AssignmentAdmin(admin.ModelAdmin):
    """Manage the assignments model"""
    list_display = ["issue", "assigned_to", "is_completed", "assigned_at"]
    search_fields = ["issue", "assigned_to", "is_completed"]


admin.site.register(Assignment, AssignmentAdmin)
