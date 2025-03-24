from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count , Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import TaskForm
from manager.models import Task, Worker, Project, Team


@login_required
def index(request):
    completed_tasks = Task.objects.filter(is_completed=True, assignees=request.user).count()
    in_process_tasks = Task.objects.filter(is_completed=False, assignees=request.user).count()
    users = Worker.objects.annotate(
        completed_tasks_count=Count("tasks_assigned", filter=Q(tasks_assigned__is_completed=True)),
        in_progress_tasks_count=Count("tasks_assigned", filter=Q(tasks_assigned__is_completed=False))
    ).select_related("position", "team")
    user_task = Task.objects.filter(assignees=request.user)

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "completed_tasks": completed_tasks,
        "in_process_tasks": in_process_tasks,
        "user_task": user_task,
    }


    return render(request, "home/index.html", context=context)


class TaskManagementList(generic.ListView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "tasks"
    template_name = "home/task_management.html"
    paginate_by = 10


class TaskManagementDetail(generic.DetailView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "tasks"
    template_name = "home/task_management_detail.html"


class TaskManagementCreate(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task_management")
    template_name = "home/task_form.html"


class TaskManagementUpdate(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "home/task_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:task_management_detail", kwargs={"pk": self.object.pk})


class TaskManagementDelete(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task_management")
    template_name = "home/task_confirm_delete.html"


class ProjectManagement(generic.ListView):
    model = Project
    queryset = Project.objects.all()
    context_object_name = "projects"
    template_name = "home/project_management.html"


class ProjectManagementDetail(generic.DetailView):
    model = Project
    queryset = Project.objects.all()
    context_object_name = "projects"
    template_name = "home/project_management_detail.html"


class TeamManagement(generic.ListView):
    model = Team
    queryset = Team.objects.all()
    context_object_name = "teams"
    template_name = "home/team_management.html"


class TeamManagementDetail(generic.DetailView):
    model = Team
    queryset = Team.objects.all()
    context_object_name = "teams"
    template_name = "home/team_management_detail.html"


class CurrentUserProfile(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()
    context_object_name = "user"
    template_name = "home/user_profile.html"

    def get_object(self, **kwargs):
        return Worker.objects.get(pk=self.request.user.pk)

class UserProfile(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()
    context_object_name = "user"
    template_name = "home/user_profile.html"


def help_page(request):
    return render(request, "home/help.html")