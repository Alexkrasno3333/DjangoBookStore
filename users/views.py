from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from users.forms import UserRegisterForm
import logging
logger = logging.getLogger(__name__)

class UserLogin(LoginView):
    template_name = "user_login.html"
    def form_valid(self, form):
        user = form.get_user()
        logger.info(f"User {user.username} logged in")
        return super().form_valid(form)


class UserLogout(LogoutView):
    next_page = reverse_lazy("books:home_page")

class UserRegister(CreateView):
    form_class = UserRegisterForm
    template_name = "users/user_register.html"
    success_url = reverse_lazy("users:login")



# def register_user(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect("users:login")
#     else:
#         form = RegisterForm()
#
#     return render(request, "users/register.html", {"form": form})
#
#
# def login_user(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect("books:home_page")
#     else:
#         form = AuthenticationForm()
#
#     return render(request, "users/login.html", {"form": form})
#
#
# def logout_user(request):
#     logout(request)
#     return redirect("books:home_page")