from django.shortcuts import render, redirect
from django.contrib import messages # to display the messages
from .models import Issue # the issue model
from accounts.models import CustomUser # the user
from .forms import IssueSubmissionForm # form to submit the issue details
from django.core.mail import send_mail # to send mail
from django.conf import settings # to configure the mail
from django.contrib.auth.decorators import login_required


# Create your views here.
# The issue data form submission
@login_required(login_url='accounts:login') # user must be logged in to submit the issue
def submit_issue(request):
    if request.method == 'POST':
        form = IssueSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()

            # Send the email upon success
            # The email variables
            # Client
            client_subject = "Issue submitted succefully"
            client_message = "Your issue has been received, and is being worked on. Your ticket number is {}. For any enquries, please contact the ICT Support".format(issue.ticket_number)
            sender_email = settings.EMAIL_HOST_USER
            receipient_email = [request.user.email]
            send_mail(
                client_subject,
                client_message,
                sender_email,
                receipient_email,
                fail_silently=False,
                )
            
            # Admin
            admin_subject = "A new issue {} submitted".format(issue.ticket_number)
            admin_message = "Please login and check out the issue, for more information"
            sender_email = settings.EMAIL_HOST_USER
            receipient_email = ["gitongadenzel@gmail.com"]
            send_mail(
                admin_subject,
                admin_message,
                sender_email,
                receipient_email,
                fail_silently=False
            )

            # Upon success of the above
            messages.success(request, "Congratulations! Your issue has been submitted successful, and the support team has been notified. Please check your email to receive your issue number")
            return redirect('accounts:home')
        else:
            messages.error(request, "Oops! Something went wrong, issue not submitted. Please consult the ICT Support Team for assistance")
    else:
        form = IssueSubmissionForm()
    context = {'form': form}
    return render(request, "clients/upload.html", context)

