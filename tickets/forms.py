from django import forms

from .models import Ticket

# The Ticket submission form
class TicketSubmissionForm(forms.ModelForm):
    """Present the Ticket model fields"""
    class Meta:
        model = Ticket
        fields = ['description', 'attachment'] # The fields filled by the user