from collections.abc import Iterable
from django.db import models
from clients.models import Issue # import the Issues model
from accounts.models import CustomUser # get the user
from tasks.models import AssignedTask

# Create your models here.
class Assignment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE) # get the issue in particular
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assignments") # get the user assigned to
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    
    # Once assigned, also reflect in the assigned task model in tasks
    def save(self, *args, **kwargs):
        """Save in assigned tasks too-- for the django admin site """
        created = not self.pk # check if the assignment instance is being created for the first time
        super().save(*args, **kwargs) # Call the save method of the super class model in Assignment

        if created: # if the assignment is being created for the first time, create an AssignedTask
            AssignedTask.objects.create(
                support_staff = self.assigned_to, # the assigned to staff
                issue = self.issue, # set the issue field of the assigned task
                
            )
        

    def __str__(self):
        return "Assignment {}".format(self.id)