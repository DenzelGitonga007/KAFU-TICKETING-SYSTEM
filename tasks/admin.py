from django.contrib import admin

# Register your models here.
from .models import AssignedTask
from accounts.models import CustomUser

# Manage the assigned tasks
class AssignedTaskAdmin(admin.ModelAdmin):
    """Manage the assigned task for support staff side"""
    list_display = ["support_staff", "issue", "progress_status", "updated_at", "details"]
    search_fields = ["support_staff", "issue", "progress_status", "updated_at", "details"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "support_staff":
            kwargs["queryset"] = CustomUser.objects.filter(user_type='support_staff')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(AssignedTask, AssignedTaskAdmin)