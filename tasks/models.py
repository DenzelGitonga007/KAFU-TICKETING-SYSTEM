from django.db import models

from accounts.models import CustomUser # for the user
from clients.models import Issue # for the issue at hand

# Create your models here.
# Assignments for the staff
class AssignedTask(models.Model):
    """The tasks for the staff"""
    support_staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    progress_choices = [
        ('unseen', 'Unseen'),
        ('ongoing', 'Ongoing'),
        ('incapable', 'Ongoing'),
        ('completed', 'Completed')
    ]
    progress_status = models.CharField(max_length=10, choices=progress_choices, default='unseen')
    details = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)