from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate, logout
from accounts.models import CustomUser # to display the users
from clients.models import Issue # to display the issues

# Create your views here.

# Home
def home(request):
    """Landing page"""
    # if admin is logged in
    if request.user.is_superuser:
        support_staff_users = CustomUser.objects.filter(user_type='support_staff') # get the support staff
        client_users = CustomUser.objects.filter(user_type='client') # get the clients
        all_issues = Issue.objects.all() # get all issues
        context = {
            'support_staff_users': support_staff_users, # render the support staff
            'client_users': client_users, # render the clients
            'all_issues': all_issues, # render the issues submitted
        }
        return render(request, 'index.html', context)
    else:
        issues = Issue.objects.filter(user=request.user) # get the issues of the particular client
        context = {
            'issues': issues
            }
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
    """Logout the user"""
    logout(request)
    return redirect('accounts:home')
