from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

class UserLogin(LoginView):
    template_name = "user_login.html"

class UserLogout(LogoutView):
    next_page = reverse_lazy("books:home_page")

class UserRegister(CreateView):
    form_class = UserCreationForm
    template_name = "users/user_register.html"
    success_url = reverse_lazy("users:login")