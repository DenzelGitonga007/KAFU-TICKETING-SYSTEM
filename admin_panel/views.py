from django.shortcuts import render, redirect
from django.contrib import messages # for dialog messages
from django.contrib.auth.decorators import user_passes_test # for logged in admin users only
from .models import Assignment # the assignement model
from accounts.models import CustomUser # for the user
from clients.models import Issue # for all issues
from .forms import AssignmentForm # the customized assignment form
from django.conf import settings # to get the settings, sender email if needed
from django.core.mail import send_mail # to send the mail


# Create your views here.
def is_superuser(user):
    """Test whether user is admin, and is admin"""
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser ,login_url='accounts:login') # admin must be logged in
# Assignment model
def admin_panel(request):
    # Retrieve all issues
    issues = Issue.objects.all()

    # Retrieve the support staff
    support_staff = CustomUser.objects.filter(user_type="support_staff")

    # Retrieve all assignments
    assignments = Assignment.objects.select_related('issues', 'assigned_to').all()


    # Assign issues
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
                return redirect('accounts:home')
            except Exception as e:
                messages.error(request, "Failed to send email notification: {}".format(str(e)))
        else:
            messages.error(request, "Oops! Something went wrong. Please check the form for errors and try again.")

    else:
        form = AssignmentForm()
    context = {
        "form": form,
        "issues": issues,
        "support_staff": support_staff,
        "assignments": assignments,
        }
    return render(request, "admin_panel/home.html", context)

