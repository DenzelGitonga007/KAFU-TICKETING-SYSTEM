from django.contrib import admin

# Register your models here.
from .models import CustomUser

# Users' model
class CustomUserAdmin(admin.ModelAdmin):
    """Manage the users"""
    list_display = ['username', 'user_type', 'is_superuser'] # fields to display
    search_fields = ['username', 'user_type'] # fields to search

    def __str__(self):
        """Stringify the data"""
        return "{}".format(self.username)
    
# Register the admin models
admin.site.register(CustomUser, CustomUserAdmin)
