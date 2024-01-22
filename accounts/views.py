from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate

# Create your views here.

# Home
def home(request):
    """Landing page"""
    context = {} # to be updated
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
