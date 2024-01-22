from django.shortcuts import render, redirect
from django.contrib import messages # to display the messages
from .models import Ticket # the Ticket model
from accounts.models import CustomUser # the user
from .forms import TicketSubmissionForm # form to submit the Ticket details
from django.core.mail import send_mail # to send mail
from django.conf import settings # to configure the mail


# Create your views here.
# The ticket data form submission
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Send the email upon success
            # The email variables
            # Client
            client_subject = "Issue submitted succefully"
            client_message = "Your issue has been received, and is being worked on. Your ticket number is {}. For any enquries, please contact the ICT Support".format(ticket.ticket_number)
            sender_email = settings.EMAIL_HOST_USER
            receipient_email = ["denzelgitonga007@gmail.com"]
            send_mail(
                client_subject,
                client_message,
                sender_email,
                receipient_email,
                fail_silently=False,
                )
            
            # Admin
            admin_subject = "A new issue {} submitted".format(ticket.ticket_number)
            admin_message = "Please login and find check out the issue, for more information"
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
            messages.success(request, "Congratulations! Your issue has been submitted successful, and the support team has been notified. Please check your email to receive your ticket number")
            return redirect('accounts:home')
        else:
            messages.error(request, "Oops! Something went wrong, issue not submitted. Please consult the ICT Support Team for assistance")
    else:
        form = TicketSubmissionForm()
    context = {'form': form}
    return render(request, "tickets/upload.html", context)

