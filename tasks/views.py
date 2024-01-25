from django.shortcuts import render, redirect
from django.contrib import messages # for dialog messages
from django.contrib.auth.decorators import login_required # to allow just logged in users
from django.core.mail import send_mail # to send mails
from .models import AssignedTask # for the Assigned tasks model
from accounts.models import CustomUser # for the user
from admin_panel.models import Assignment
from clients.models import Issue # the issues submitted
from .forms import TaskProgressForm

# Create your views here.

# Update the task progress
@login_required(login_url="accounts:login")
def update_task(request, issue_id):
    """Update the task"""
    issue = Issue.objects.get(pk=issue_id) # this issue should also reference the support staff assigned to it-- each support staff to only access issues assigned to them
    if request.method == "POST":
        form = TaskProgressForm(request.POST)
        if form.is_valid():
            task_progress = form.save(commit=False)
            task_progress.support_staff = request.user # the signed in user
            task_progress.issue = issue # the particular issue
            task_progress.save()

            # Send the email to notify the admin that the issue has been updated

            # Display success message if successful
            messages.success(request, "Issue updated successfully")
            return redirect("accounts:home")
        else:
            messages.error(request, "Oops! Something went wrong")
    else:
        form = TaskProgressForm()
    context = {
        'form': form,
        'issue': issue
    }

    return render(request, "tasks/update_task.html", context)


# Support staff views the tasks assigned to them
@login_required(login_url="accounts:login")
def assigned_tasks(request):
    """Retrieve the tasks of the support staff"""
    support_staff = request.user

    # Retrieve just the tasks assigned to the support staff
    assigned_tasks = Assignment.objects.filter(assigned_to=support_staff)

    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, "tasks/tasks.html", context)