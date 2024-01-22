from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


# Custom Registration form
class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    class Meta(UserCreationForm.Meta):
        """Inherit the default Meta fields of user creation"""
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('user_type', 'email') # Allow the user to select the type of user they are

# Custom Login form
class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form"""
    class Meta():
        """Inherit the default meta fields for user login"""
        model = CustomUser