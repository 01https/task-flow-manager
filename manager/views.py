from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count , Q
from django.shortcuts import render
from django.views import generic

from manager.models import Task, Worker


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
