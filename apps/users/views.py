from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

class CustomLoginView(LoginView):
    template_name = "users/login.html"

class CustomLogoutView(LogoutView):
    next_page = "/"