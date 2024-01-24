from django.db import models
from clients.models import Issue # import the Issues model
from accounts.models import CustomUser # get the user

# Create your models here.
class Assignment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE) # get the issue in particular
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assignments") # get the user assigned to
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return "Assignment {}".format(self.id)