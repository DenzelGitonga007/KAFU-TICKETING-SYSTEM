from django.db import models
from accounts.models import CustomUser # Users model


import uuid # for random universal unique identifier

# Generate the unique Ticket number
def generate_ticket_number():
    """Generate the ticket number"""
    return str(uuid.uuid4()) # eg '550e8400-e29b-41d4-a716-446655440000'

# Upload file
def upload_path(instance, filename):
    """Where to upload the file"""
    return "ticket_attachment/{}/{}/{}".format(generate_ticket_number(), (instance.user.username), filename) # ticket_attachement/ticket_number/username/filename

# Create your models here.

# Ticket model
class Issue(models.Model):
    """The issue details"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=255, unique=True, default=generate_ticket_number, editable=False) # should be assigned by default
    description = models.TextField()
    attachment = models.FileField(upload_to=upload_path) 
    # upload to ticket_attachement/username
    # also be able to upload both voice note, and screenshots at the same time/at a go
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.ticket_number, self.user)

