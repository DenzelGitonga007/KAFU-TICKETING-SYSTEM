from django import forms


from .models import Assignment # assignment model
from accounts.models import CustomUser # User model, to get the user_type

# Assignement form-- setting the user_type as only support staff
class AssignmentForm(forms.ModelForm):
    """Form for assigning the support staff"""
    class Meta:
        model = Assignment
        fields = ["issue", "notes","assigned_to"]

        def __init__(self, *args, **kwargs):
           super(AssignmentForm, self).__init__(*args, **kwargs)
           # Filter to display only the support staff
           self.fields["assigned_to"].queryset = CustomUser.objects.filter(user_type="support_staff")


        
# Update the assignment
class UpdateAssignmentForm(forms.ModelForm):
    """Admin updates the assignment"""
    class Meta:
        model = Assignment
        fields = ['notes', 'assigned_to', 'is_completed']
        