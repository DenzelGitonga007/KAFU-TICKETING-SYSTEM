from django.urls import path
from . import views
app_name = "tasks"

urlpatterns = [
    path('update_task/<int:issue_id>/', views.update_task, name="update_task"), # update the task
    path('tasks_list/', views.assigned_tasks, name="list_tasks") # list the assigned tasks
]