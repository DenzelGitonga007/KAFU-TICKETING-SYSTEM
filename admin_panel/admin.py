from django.contrib import admin

# Register your models here.
from .models import Assignment # Assignment model
from accounts.models import CustomUser # User model, for the user_type
from .forms import AssignmentForm

# Assignment admin
class AssignmentAdmin(admin.ModelAdmin):
    """Manage the assignments model"""
    list_filter = ('assigned_to', 'issue')
    list_display = ["issue", "assigned_to", "is_completed", "assigned_at"]
    search_fields = ["issue__ticket_number", "assigned_to__username", "is_completed"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "assigned_to":
            kwargs["queryset"] = CustomUser.objects.filter(user_type='support_staff')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    


admin.site.register(Assignment, AssignmentAdmin)
