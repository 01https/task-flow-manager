from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Task, Project, Team, TaskType, ProjectType, Position

Worker = get_user_model()


class ViewsTestCase(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Development")
        self.project_type = ProjectType.objects.create(name="Web")
        self.position = Position.objects.create(name="Developer")

        self.user = Worker.objects.create(
            username="testuser",
            password="testpass123",
            position=self.position
        )

        self.team = Team.objects.create(name="Dev Team")
        self.project = Project.objects.create(
            name="Website",
            type=self.project_type
        )
        self.task = Task.objects.create(
            name="Fix bugs",
            task_type=self.task_type,
            project=self.project,
            deadline="2023-12-31"
        )
        self.task.assignees.add(self.user)
        self.task.teams.add(self.team)

    def test_index_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manager:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fix bugs", response.content)

    def test_help_page_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manager:help'))
        self.assertEqual(response.status_code, 200)

    def test_task_management_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manager:task_management'))
        self.assertEqual(response.status_code, 200)

    def test_task_management_detail_view(self):
        self.client.force_login(self.user)
        url = reverse('manager:task_management_detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_task_management_create_view(self):
        self.client.force_login(self.user)
        url = reverse('manager:task_create')

        form_data = {
            'name': 'New Task',
            'description': 'Test task description',
            'deadline': '2023-12-31',
            'priority': 'Middle',
            'task_type': self.task_type.pk,
            'project': self.project.pk,
            'assignees': [self.user.pk],
            'teams': [self.team.pk],
        }

        response = self.client.post(url, form_data)

        if response.status_code != 302:
            print("Form errors:",
                  response.context['form'].errors if 'form' in response.context else "No form in context")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

        new_task = Task.objects.get(name='New Task')
        self.assertEqual(new_task.assignees.count(), 1)
        self.assertEqual(new_task.teams.count(), 1)

    def test_project_management_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manager:project_management'))
        self.assertEqual(response.status_code, 200)

    def test_team_management_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manager:team_management'))
        self.assertEqual(response.status_code, 200)

    def test_current_user_profile_view(self):
        self.client.force_login(self.user)
        url = reverse('manager:user_profile', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
