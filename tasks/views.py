from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages # for dialog messages
from django.contrib.auth.decorators import login_required # to allow just logged in users
from django.core.mail import send_mail # to send mails
from django.conf import settings # to access the email of the host
from admin_panel.models import Assignment # to view and update the assignment from the admin_panel
from .forms import UpdateTaskForm # the update task form


# Create your views here.

# Support staff views the tasks assigned to them
@login_required(login_url="accounts:login")
def assigned_tasks(request):
    """Retrieve the tasks of the support staff"""
    
    # Retrieve just the tasks assigned to the support staff
    assigned_tasks = Assignment.objects.filter(assigned_to=request.user) # for the Assignment model
   
    context = {
        'assigned_tasks': assigned_tasks,
    }
    return render(request, "tasks/tasks.html", context)

# Update the task
@login_required(login_url="accounts:login")
def update_tasks(request, task_id):
    """Update the assigned tasks"""
    # Get the logged in user
    staff = request.user
    # Get the assigned task
    task = get_object_or_404(Assignment, id=task_id, assigned_to=staff) # get the particular assignment as task
    if request.method == "POST":
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            # save the form and check the status
            updated_task = form.save()
            if updated_task.progress_status == "completed": # Notify the admin if task is marked completed by the staff
                subject = "Task Completed by {}".format(staff.username)
                message = 'Task {} has been marked as complete by {}. Please review and approve.'.format(updated_task.issue.ticket_number, staff.username)
                system_email = settings.EMAIL_HOST_USER # sender email
                admin_email = settings.EMAIL_HOST_USER # recepient email
                try:
                    send_mail(subject, message, system_email, [admin_email], fail_silently=False)
                    messages.success(request, "Task marked completed, and admin has been notified")
                except Exception as e:
                    messages.error(request, "Failed to send notification to the admin: {}".format(str(e)))
            else:
                messages.success(request, "Task updated successfully.")
                # send the email
                subject = "Task update from {}".format(staff.username)
                message = "Please log in and affirm that task {} is ready to be marked complete".format(task.issue.ticket_number)
                system_email = settings.EMAIL_HOST_USER # sender email
                admin_email = settings.EMAIL_HOST_USER # recepient email

                try:
                    send_mail(subject, message, system_email, [admin_email], fail_silently=False)

                except Exception as e:
                    messages.error(request, "Failed to send the email notification {} to the admin".format(str(e)))

            messages.success(request, "Task updated successfully")
            return redirect("accounts:home") # return to the home page
        else:
            messages.error(request, "Oops! Task not updated... please try again or contact ICT Support Admin")
    else:
        form = UpdateTaskForm(instance=task)
    
    # To the template
    context = {
        'form': form,
        'task': task
    }
    return render(request, "tasks/update_task.html", context)




