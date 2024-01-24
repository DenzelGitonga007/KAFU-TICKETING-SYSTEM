from django.urls import path
from . import views


app_name = 'clients'

urlpatterns = [
    path('submit_issue/', views.submit_issue, name="submit_issue")
]