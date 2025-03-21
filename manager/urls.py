from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from manager.views import index, TaskManagementList, TaskManagementDetail

app_name = "manager"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", index, name="index"),
    path("task-management", TaskManagementList.as_view(), name="task_management"),
    path("task-management/<int:pk>/", TaskManagementDetail.as_view(), name="task_management_detail")
]
