from django.urls import path
from . import views
app_name = 'tickets'

urlpatterns = [
    path('submit_issue/', views.submit_ticket, name="submit_ticket")
]