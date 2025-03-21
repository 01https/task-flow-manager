from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Middle", "Middle"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=7,
        choices=PRIORITY_CHOICES,
        default="Middle"
    )
    task_type = models.ForeignKey("TaskType", on_delete=models.PROTECT)
    assignees = models.ManyToManyField("Worker", related_name="tasks_assigned")
    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        related_name="tasks_project"
    )
    teams = models.ManyToManyField("Team", related_name="tasks_team")

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(
        "ProjectType",
        on_delete=models.PROTECT
    )
    teams = models.ManyToManyField(
        "Team",
        related_name="projects_team",
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="workers",
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="members",
    )

    def __str__(self):
        return self.username