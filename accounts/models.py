from django.db import models
from django.contrib.auth.models import AbstractUser # Reference the default user model


# Create your models here.
# The customized user model
class CustomUser(AbstractUser):
    """The custom user model, from the default user model"""
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('support_staff', 'Support_staff')
    ] # represent the type of users-- client, is db name, Client, is name on front-end

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='client') # the user type field, referencing the USER_TYPE_CHOICES
    email = models.EmailField(unique=True)
    # Other fields to be added here

    # Get the fullname
    def get_full_name(self):
        """Get fullname"""
        if self.first_name and self.last_name:
            """Combine these and return the name"""
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username
        
    
    def __str__(self):
        """Stringify the values"""
        return self.username