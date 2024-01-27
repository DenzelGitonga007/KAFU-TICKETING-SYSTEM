from django import forms
from admin_panel.models import Assignment # to update the Assginment fields

# Update Assignment form
class UpdateTaskForm(forms.ModelForm):
    """Update the Assignment model field"""
    class Meta:
        model = Assignment
        fields = ["notes", "progress_status"]