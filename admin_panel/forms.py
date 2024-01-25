from django import forms

from .models import Assignment

# Assignement form-- setting the user_type as only support staff
class AssignmentForm(forms.ModelForm):
    """Form for assigning the support staff"""
    class Meta:
        model = Assignment
        fields = "__all__"

        # Get the user_type as only support staff
        def clean_assigned_to(self):
            assigned_to = self.cleaned_data["assigned_to"]
            user_type = getattr(assigned_to, 'user_type', None)

            if user_type != "support_staff": # Retrieve just the support staff
                raise forms.ValidationError("Only support staff can be assigned tasks")
            
            return assigned_to
        
        