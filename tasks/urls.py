from django.urls import path
from . import views
app_name = "tasks"

urlpatterns = [
    
    path('tasks_list/', views.assigned_tasks, name="list_tasks") # list the assigned tasks
]