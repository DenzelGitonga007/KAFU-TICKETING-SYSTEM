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

            # Upon success of the above
            messages.success(request, "Congratulations! Your issue has been submitted successful, and the support team has been notified. Please check your email to receive your ticket number")
            return redirect('accounts:home')
        else:
            messages.error(request, "Oops! Something went wrong, issue not submitted. Please consult the ICT Support Team for assistance")
    else:
        form = TicketSubmissionForm()
    context = {'form': form}
    return render(request, "tickets/upload.html", context)

