from django import forms
from .models import AssignedTask # to enter data into the model

# Customized form to update the tasks
class TaskProgressForm(forms.ModelForm):
    """Update the tasks"""
    class Meta:
        model = AssignedTask
        fields = ["progress_status", "details"]
    