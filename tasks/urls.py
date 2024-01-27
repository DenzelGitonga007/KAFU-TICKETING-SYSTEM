from django.urls import path
from . import views
app_name = "tasks"

urlpatterns = [
    path('tasks_list/', views.assigned_tasks, name="list_tasks"), # list the assigned tasks
    path('update_task/<int:task_id>', views.update_tasks, name="update_task")
]