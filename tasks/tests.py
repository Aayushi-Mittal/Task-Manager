from django.test import TestCase, Client

from tasks.models import Task, User


class TestTaskManager(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test123")
        self.client.login(username="testuser", password="12345")
        self.task = Task.objects.create(
            title="create test task",
            description="some description",
            priority=1,
            user=self.user,
        )

    def test_task_create(self):
        self.assertTrue(
            Task.objects.filter(user=self.user, title="create test task").exists()
        )
        self.assertEqual(str(self.task), "create test task")

    def test_task_read(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)

    def test_task_update(self):
        temp_data = {
            "title": "Updated test",
            "description": "Test description",
            "priority": 1,
            "status": "PENDING",
        }
        response = self.client.post(f"/update-task/{self.task.id}/", temp_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.objects.first().title, "Updated test")

    def test_task_delete(self):
        response = self.client.get(f"/delete-task/{self.task.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.objects.first().deleted, True)

    def test_task_priority_increment(self):
        task1 = Task.objects.create(
            title="test title",
            description="test description",
            priority=1,
            user=self.user,
        )
        Task.objects.create(
            title="test title",
            description="test description",
            priority=1,
            user=self.user,
        )
        task1 = Task.objects.get(pk=task1.pk)
        self.assertEqual(task1.priority, 1)


    def test_task_priority_does_not_increment(self):
        task1 = Task.objects.create(
            title="test title",
            description="test description",
            priority=1,
            user=self.user,
        )
        Task.objects.create(
            title="test title",
            description="test description",
            priority=1,
            status="COMPLETED",
            user=self.user,
        )
        task1 = Task.objects.get(pk=task1.pk)
        self.assertEqual(task1.priority, 1)

    def test_api(self):
        response = self.client.get("/api/v1/task/")
        self.assertEqual(response.status_code, 403)
