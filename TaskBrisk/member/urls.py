from django.urls import path
from .views import *
from .dashboardviews import *

urlpatterns = [
    path("user-register/", user_register,name="user_register"),
    path("user-login/", user_login,name='user_login'),
    path("forgot-password/", forgot_password,name='forgot_password'),
    path("reset-password/", reset_password, name='reset_password'),
    path("home/", home_dashboard, name='home_dashboard'),

]
