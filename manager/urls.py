from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from manager.views import index, TaskManagementList, TaskManagementDetail, ProjectManagementDetail, ProjectManagement, \
    TeamManagement, TeamManagementDetail, help_page, CurrentUserProfile, UserProfile, TaskManagementCreate, \
    TaskManagementUpdate, TaskManagementDelete, ProjectManagementCreate, ProjectManagementUpdate, \
    ProjectManagementDelete

app_name = "manager"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", index, name="index"),
    path("task-management/", TaskManagementList.as_view(), name="task_management"),
    path("task-management/<int:pk>/", TaskManagementDetail.as_view(), name="task_management_detail"),
    path("task/create/", TaskManagementCreate.as_view(), name="task_create"),
    path("task/update/<int:pk>/", TaskManagementUpdate.as_view(), name="task_update"),
    path("task/<int:pk>/delete/", TaskManagementDelete.as_view(), name="task_delete"),
    path("project-management/", ProjectManagement.as_view(), name="project_management"),
    path("project-management/<int:pk>/", ProjectManagementDetail.as_view(), name="project_management_detail"),
    path("project/create/", ProjectManagementCreate.as_view(), name="project_create"),
    path("project/<int:pk>/update/", ProjectManagementUpdate.as_view(), name="project_update"),
    path("project/<int:pk>/delete", ProjectManagementDelete.as_view(), name="project_delete"),
    path("team-management/", TeamManagement.as_view(), name="team_management"),
    path("team-management/<int:pk>/", TeamManagementDetail.as_view(), name="team_management_detail"),
    path("help/", help_page, name="help"),
    path("profile/", CurrentUserProfile.as_view(), name="current_profile"),
    path("profile/<int:pk>/", UserProfile.as_view(), name="user_profile")
]
