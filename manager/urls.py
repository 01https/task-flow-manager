from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from manager.views import index


app_name = "manager"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", index, name="index")
]
