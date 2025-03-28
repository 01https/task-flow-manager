from django.test import TestCase
from django.contrib.auth import get_user_model
from manager.models import TaskType, Task, ProjectType, Project, Team, Position

Worker = get_user_model()


class TaskTypeModelTest(TestCase):
    def test_task_type_creation(self):
        task_type = TaskType.objects.create(name="Development")
        self.assertEqual(str(task_type), "Development")
        self.assertEqual(TaskType.objects.count(), 1)


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug Fixing")
        self.project_type = ProjectType.objects.create(name="Web")
        self.team = Team.objects.create(name="Development Team")
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create_user(
            username="testuser",
            password="testpass123",
            position=self.position,
            team=self.team
        )
        self.project = Project.objects.create(
            name="Website",
            type=self.project_type
        )

    def test_task_creation(self):
        task = Task.objects.create(
            name="Fix Login Page",
            description="Fix authentication bug",
            deadline="2023-12-31",
            priority="High",
            task_type=self.task_type,
            project=self.project
        )
        task.assignees.add(self.user)
        task.teams.add(self.team)

        self.assertEqual(str(task), "Fix Login Page")
        self.assertEqual(task.assignees.count(), 1)
        self.assertEqual(task.teams.count(), 1)
        self.assertEqual(task.priority, "High")
        self.assertFalse(task.is_completed)


class ProjectTypeModelTest(TestCase):
    def test_project_type_creation(self):
        project_type = ProjectType.objects.create(name="Mobile App")
        self.assertEqual(str(project_type), "Mobile App")
        self.assertEqual(ProjectType.objects.count(), 1)


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project_type = ProjectType.objects.create(name="AI")
        self.team = Team.objects.create(name="AI Team")

    def test_project_creation(self):
        project = Project.objects.create(
            name="Chatbot",
            type=self.project_type,
            description="AI chatbot for support"
        )
        project.teams.add(self.team)

        self.assertEqual(str(project), "Chatbot")
        self.assertEqual(project.teams.count(), 1)
        self.assertEqual(project.type.name, "AI")


class TeamModelTest(TestCase):
    def test_team_creation(self):
        team = Team.objects.create(
            name="QA Team",
            description="Testing team"
        )
        self.assertEqual(str(team), "QA Team")
        self.assertEqual(Team.objects.count(), 1)


class PositionModelTest(TestCase):
    def test_position_creation(self):
        position = Position.objects.create(name="Project Manager")
        self.assertEqual(str(position), "Project Manager")
        self.assertEqual(Position.objects.count(), 1)


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Designer")
        self.team = Team.objects.create(name="Design Team")

    def test_worker_creation(self):
        worker = Worker.objects.create_user(
            username="designer1",
            password="testpass123",
            position=self.position,
            team=self.team
        )
        self.assertEqual(str(worker), "designer1")
        self.assertEqual(worker.position.name, "Designer")
        self.assertEqual(worker.team.name, "Design Team")
        self.assertTrue(worker.check_password("testpass123"))
