from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages # for dialog messages
from django.contrib.auth.decorators import user_passes_test # for logged in admin users only
from .models import Assignment # the assignement model
from accounts.models import CustomUser # for the user
from clients.models import Issue # for all issues
from .forms import AssignmentForm, UpdateAssignmentForm # the customized assignment form, and the update one
from django.conf import settings # to get the settings, sender email if needed
from django.core.mail import send_mail # to send the mail


# Create your views here.
def is_superuser(user):
    """Test whether user is admin, and is admin"""
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser ,login_url='accounts:login') # admin must be logged in
# Home model
def admin_panel_home(request):
    # Fetch all items to be rendered onto the Front end
    support_staff_users = CustomUser.objects.filter(user_type='support_staff') # get the support staff
    client_users = CustomUser.objects.filter(user_type='client') # get the clients
    all_issues = Issue.objects.all() # get all issues
    assignments = Assignment.objects.select_related('issue', 'assigned_to').all() # Retrieve all assignments
    # Render to the Front end
    context = {
        'support_staff_users': support_staff_users, # render the support staff
        'client_users': client_users, # render the clients
        'all_issues': all_issues, # render the issues submitted
        "assignments": assignments,
        }
    return render(request, "admin_panel/home.html", context)


@user_passes_test(is_superuser, login_url='accounts:login') # admin must be logged in
# Assignment model
def assign_view(request):
    # Assign issues
    # Get the support staff only
    support_staffs = CustomUser.objects.filter(user_type='support_staff')
    issues = Issue.objects.all()
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment_instance = form.save() # the variable for the form instances
            
            # Send email to the support staff that a new assignment was done
            subject = "A new assignment issue {}".format(assignment_instance.issue.ticket_number) # obtain the ticket number of the issue assigned
            message = "Please log in and find more details about the issue"
            admin_email = request.user.email # the email of the logged in user/admin
            support_staff_email = assignment_instance.assigned_to.email # get the email of the support staff

            try:
                # Send the email now
                send_mail(subject, message, admin_email, [support_staff_email], fail_silently=False)
                
                # display success that the assigment was done
                messages.success(request, "Issue assigned to {} successfully".format(assignment_instance.assigned_to.username))
                # return to home page for admin
                return redirect('admin_panel:admin_panel_home')
            except Exception as e:
                messages.error(request, "Failed to send email notification: {}".format(str(e)))
        else:
            messages.error(request, "Oops! Something went wrong. Please check the form for errors and try again.")

    else:
        form = AssignmentForm()
    context = {
        "form": form,
        "support_staffs": support_staffs,
        "issues": issues,
    }
    return render(request, 'admin_panel/assign.html', context)
    
# Update the assignment
@user_passes_test(is_superuser, login_url='accounts:login') # admin must be logged in
def update_assignment_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = UpdateAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            updated_assignment = form.save() # save the form as updated_assignment variable
            # Send email to client if the task is marked complete
            if updated_assignment.is_completed:
                subject = "Your issue has been solved"
                message = "Dear {}, your issue with ticket number {} has been solved. If you have any enquiries, visit the ICT Offices for further assistance. Nonetheless, hope we have been helpful to you. Feel free to submit any other issue you may be having. Thank you.".format(assignment.issue.user, assignment.issue.ticket_number)
                system_email = settings.EMAIL_HOST_USER # sender's email
                client_email = assignment.issue.user.email # recipient's email
                try:
                    send_mail(subject, message, system_email, [client_email], fail_silently=False)
                    messages.success(request, "Task completed, and client has been updated")
                except Exception as e:
                    messages.error(request, "Failed to notify the client about solving the issue")
            # Upon successful update
            messages.success(request, "Task updated successfully")
            return redirect('admin_panel:admin_panel_home')
        else:
            messages.error(request, "Oops! Task not updated... please try again")

    else:
        form = UpdateAssignmentForm(instance=assignment)
    # The template
    context = {
        'form': form,
        'assignment': assignment
    }
    return render(request, 'admin_panel/update_assignment.html', context)
