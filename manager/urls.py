from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from manager.views import index, TaskManagementList, TaskManagementDetail, ProjectManagementDetail, ProjectManagement, \
    TeamManagement, TeamManagementDetail, help_page

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
    path("task-management/<int:pk>/", TaskManagementDetail.as_view(), name="task_management_detail"),
    path("project-management", ProjectManagement.as_view(), name="project_management"),
    path("project-management/<int:pk>", ProjectManagementDetail.as_view(), name="project_management_detail"),
    path("team-management", TeamManagement.as_view(), name="team_management"),
    path("team-management/<int:pk>", TeamManagementDetail.as_view(), name="team_management_detail"),
    path("help/", help_page, name="help")
]
