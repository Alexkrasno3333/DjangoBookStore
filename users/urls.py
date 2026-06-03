from django.urls import path
from users import views


app_name = "users"

urlpatterns = [
    path("login/",views.UserLogin.as_view(),name="login"),
    path("logout/",views.UserLogout.as_view(),name= "logout"),

    path("register/",views.UserRegister.as_view(),name="register"),

]