from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from accounts.models import CustomUser # to display the users
from clients.models import Issue # to display the issues
# The views based on the type of user
from admin_panel.views import admin_panel_home # display the admin home page
from tasks.views import assigned_tasks # display the support staff page

# Create your views here.

# Home
def home(request):
    """
    Display the landing page.

    For authenticated users:
        - If the user is an admin, redirect to the admin panel home.
        - If the user is a support staff, redirect to the assigned tasks.

    For unauthenticated users:
        - Display the landing page with issues submitted by the user (if any).
    """
    user = request.user  # The logged-in user
    issues = Issue.objects.filter(user=user.id)  # Issues submitted by the user

    # Check if the user is authenticated/logged in
    if user.is_authenticated:
        # Check the type of user
        if user.user_type == 'admin':
            return admin_panel_home(request)
        elif user.user_type == 'support_staff':
            return assigned_tasks(request)

    context = {"issues": issues}
    
    # For unauthenticated users
    return render(request, 'index.html', context)


        



# Register user
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Congratulations! You're logged in.")
            return redirect('accounts:home') # redirect to home page after successful login/register
        else:
            # What should be here?
            messages.error(request, "Registration failed! Please try again.")
    else:
        form = CustomUserCreationForm()
    context = {'form': form}

    return render(request, 'accounts/register.html', context)

# Login user
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Congratulations! You're logged in")
            # Redirect to respective urls
            if user.user_type == 'admin': # if user is 'admin', redirect to admin url
                return redirect('admin_panel:admin_panel_home')
            elif user.user_type == 'support_staff': # if user is 'support_staff', redirect to tasks:list_tasks
                return redirect('tasks:list_tasks')
            else:
                return redirect('accounts:home') 
        else:
            # What should go here?
            messages.error(request, "Login failed! Please try again")
    else:
        form = CustomAuthenticationForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# Logout
def logout_user(request):
    """Logout"""
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have successfully logged out...")
        return redirect("accounts:home")
    context = {}
    return render(request, "accounts/logout.html", context)
