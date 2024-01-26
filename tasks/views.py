from django.shortcuts import render, redirect
from django.contrib import messages # for dialog messages
from django.contrib.auth.decorators import login_required # to allow just logged in users
from django.core.mail import send_mail # to send mails
from admin_panel.models import Assignment # to view and update the assignment from the admin_panel


# Create your views here.

# Support staff views the tasks assigned to them
@login_required(login_url="accounts:login")
def assigned_tasks(request):
    """Retrieve the tasks of the support staff"""
    support_staff = request.user

    # Retrieve just the tasks assigned to the support staff
    assigned_tasks = Assignment.objects.filter(assigned_to=support_staff) # for the Assignment model
    # assigned_tasks = AssignedTask.objects.filter(support_staff=support_staff)

    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, "tasks/tasks.html", context)