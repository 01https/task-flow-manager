from django.test import TestCase
from django.contrib.auth import get_user_model
from manager.forms import TaskForm, ProjectForm, TeamForm, WorkerForm, TaskNameSearchForm
from manager.models import TaskType, Position, Team, Project, ProjectType

Worker = get_user_model()

class FormsTestCase(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Development")
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create(
            username="testuser",
            password="testpass123",
            position=self.position
        )
        self.team = Team.objects.create(name="Dev Team")
        self.project_type = ProjectType.objects.create(name="Test Type")
        self.project = Project.objects.create(
            name="Test Project",
            type=self.project_type
        )

    def test_task_form_valid(self):
        form_data = {
            'name': 'New Task',
            'description': 'Task description',
            'deadline': '2023-12-31',
            'priority': 'Middle',
            'task_type': self.task_type.pk,
            'project': self.project.pk,
            'assignees': [self.user.pk],
            'teams': [self.team.pk]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_missing_required(self):
        form_data = {
            'name': '',
            'deadline': '2023-12-31',
            'task_type': self.task_type.pk
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_project_form_valid(self):
        form_data = {
            'name': 'New Project',
            'type': self.project_type.pk,
            'teams': [self.team.pk]
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_project_form_teams_not_required(self):
        form_data = {
            'name': 'New Project',
            'type': self.project_type.pk,
            'teams': []
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_team_form_valid(self):
        form_data = {
            'name': 'New Team',
            'members': [self.user.pk],
            'projects': [self.project.pk]
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_form_fields(self):
        form = WorkerForm()
        self.assertEqual(
            list(form.fields.keys()),
            ['username', 'first_name', 'last_name', 'position', 'email', 'team']
        )

    def test_worker_form_valid(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'Test',
            'last_name': 'User',
            'position': self.position.pk
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_search_form(self):
        form = TaskNameSearchForm(data={'name': 'search term'})
        self.assertTrue(form.is_valid())
        empty_form = TaskNameSearchForm(data={'name': ''})
        self.assertTrue(empty_form.is_valid())

    def test_task_search_form_widget_attrs(self):
        form = TaskNameSearchForm()
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Search... (name)')
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')
