from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Middle", "Middle"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
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
        "Project", on_delete=models.PROTECT,
        related_name="tasks_project"
    )
    team = models.ManyToManyField("Team", related_name="tasks_team")
