from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    TaskForm,
    ProjectForm,
    TeamForm,
    WorkerForm,
    TaskNameSearchForm
)
from manager.models import Task, Worker, Project, Team


@login_required
def index(request):
    search_query = request.GET.get("search", "")

    completed_tasks = Task.objects.filter(
        is_completed=True,
        assignees=request.user
    ).count()

    in_process_tasks = Task.objects.filter(
        is_completed=False,
        assignees=request.user
    ).count()

    users = Worker.objects.annotate(
        completed_tasks_count=Count(
            "tasks_assigned",
            filter=Q(tasks_assigned__is_completed=True)),
        in_progress_tasks_count=Count(
            "tasks_assigned",
            filter=Q(tasks_assigned__is_completed=False))
    ).select_related(
        "position",
        "team"
    ).order_by("-completed_tasks_count")

    user_task = Task.objects.filter(
        assignees=request.user
    ).order_by("is_completed")

    if search_query:
        users = users.filter(
            username__icontains=search_query
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "completed_tasks": completed_tasks,
        "in_process_tasks": in_process_tasks,
        "user_task": user_task,
        "search_query": search_query
    }

    return render(request, "home/index.html", context=context)


class TaskManagementList(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.all().order_by("is_completed")
    context_object_name = "tasks"
    template_name = "home/task_management.html"
    paginate_by = 10

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(TaskManagementList, self).get_context_data(**kwargs)

        context["search_form"] = TaskNameSearchForm()
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class TaskManagementDetail(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = "tasks"
    template_name = "home/task_management_detail.html"


class TaskManagementCreate(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task_management")
    template_name = "home/task_form.html"


class TaskManagementUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "home/task_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:task_management_detail",
            kwargs={"pk": self.object.pk}
        )


class TaskManagementDelete(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task_management")
    template_name = "home/task_confirm_delete.html"


class ProjectManagement(LoginRequiredMixin, generic.ListView):
    model = Project
    queryset = Project.objects.all()
    context_object_name = "projects"
    template_name = "home/project_management.html"


class ProjectManagementDetail(LoginRequiredMixin, generic.DetailView):
    model = Project
    queryset = Project.objects.all()
    context_object_name = "projects"
    template_name = "home/project_management_detail.html"


class ProjectManagementCreate(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("manager:project_management")
    template_name = "home/project_form.html"


class ProjectManagementUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "home/project_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:project_management_detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectManagementDelete(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:project_management")
    template_name = "home/project_confirm_delete.html"


class TeamManagement(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.all()
    context_object_name = "teams"
    template_name = "home/team_management.html"


class TeamManagementDetail(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.all()
    context_object_name = "teams"
    template_name = "home/team_management_detail.html"


class TeamManagementCreate(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("manager:team_management")
    template_name = "home/team_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        if "members" in form.cleaned_data:
            self.object.members.set(form.cleaned_data["members"])

        if "projects" in form.cleaned_data:
            self.object.projects_team.set(form.cleaned_data["projects"])

        return response


class TeamManagementUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "home/team_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:team_management_detail",
            kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)

        if "members" in form.cleaned_data:
            self.object.members.set(form.cleaned_data["members"])

        if "projects" in form.cleaned_data:
            self.object.projects_team.set(form.cleaned_data["projects"])

        return response


class TeamManagementDelete(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:team_management")
    template_name = "home/team_confirm_delete.html"


class CurrentUserProfile(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()
    context_object_name = "user"
    template_name = "home/user_profile.html"

    def get_object(self, **kwargs):
        return Worker.objects.get(pk=self.request.user.pk)


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all()
    context_object_name = "user"
    template_name = "home/user_profile.html"


class CurrentUserProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerForm
    template_name = "home/worker_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:user_profile",
            kwargs={"pk": self.object.pk}
        )

    def get_object(self, **kwargs):
        return self.request.user


@login_required
def help_page(request):
    return render(request, "home/help.html")
