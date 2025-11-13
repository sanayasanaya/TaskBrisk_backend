from django.urls import path
from .views import *

urlpatterns = [
    path("user-register/", user_register,name="user_register"),
    path("user-login/", user_login,name='user_login'),
    path("forgot-password/", forgot_password,name='forgot_password'),
    
]
