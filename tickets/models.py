from django.db import models
from accounts.models import CustomUser # Users model
# Create your models here.
# Ticket model
class Ticket(models.Model):
    """The ticket details"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=255, unique=True) # should be assigned by default
    description = models.TextField()
    attachment = models.FileField(upload_to='ticket_attachement/') 
    # upload to ticket_attachement/username
    # also be able to upload both voice note, and screenshots at the same time/at a go
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.ticket_number, self.user)

