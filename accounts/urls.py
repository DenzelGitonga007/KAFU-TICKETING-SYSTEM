from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.home, name='home'), # home page
    path('login/', views.login_user, name='login'), # login page
    path('register/', views.register, name='register'), # register page
]