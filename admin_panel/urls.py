from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path('', views.admin_panel_home, name="admin_panel_home"), # view the admin panel
    path('assign_task/', views.assign_view, name="assign"), # assign url
    path('update_assignment/<int:assignment_id>/', views.update_assignment_view, name="update_assignment") # update the assignment
]