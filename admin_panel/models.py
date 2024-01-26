from django.db import models
from clients.models import Issue # import the Issues model
from accounts.models import CustomUser # get the user


# Create your models here.
class Assignment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE) # get the issue in particular
    notes = models.TextField() # description about the issue
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assignments") # get the user assigned to
    is_completed = models.BooleanField(default=False)
    progress_choices = [
        ('unseen', 'Unseen'),
        ('ongoing', 'Ongoing'),
        ('incapable', 'Incapable'),
        ('completed', 'Completed')
    ]
    progress_status = models.CharField(max_length=10, choices=progress_choices, default='unseen')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Assignment {}".format(self.id)