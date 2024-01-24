from django import forms

from .models import Issue

# The Ticket submission form
class IssueSubmissionForm(forms.ModelForm):
    """Present the Ticket model fields"""
    class Meta:
        model = Issue
        fields = ['description', 'attachment'] # The fields filled by the user