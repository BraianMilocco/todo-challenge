from django.test import TestCase
from datetime import datetime
from login.models import MyUser
from ..models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertFalse(self.task.delete)
        self.assertFalse(self.task.completed)
        self.assertIsInstance(self.task.created_at, datetime)
        self.assertEqual(self.task.user, self.user)

    def test_get_all_from_user(self):
        Task.objects.create(
            title='Test Task 2',
            description='This is another test task',
            user=self.user
        )
        tasks = Task.get_all_from_user(self.user.id)
        self.assertEqual(tasks.count(), 2)

        tasks_filtered = Task.get_all_from_user(self.user.id, completed=False)
        self.assertEqual(tasks_filtered.count(), 2)

        tasks_filtered = Task.get_all_from_user(self.user.id, completed=True)
        self.assertEqual(tasks_filtered.count(), 0)

    def test_get_task_from_user(self):
        task_id = self.task.id
        user_id = self.user.id

        task = Task.get_task_from_user(task_id, user_id)
        self.assertEqual(task, self.task)

        task = Task.get_task_from_user(task_id, user_id + 1)  # User ID doesn't match
        self.assertIsNone(task)

        task = Task.get_task_from_user(task_id + 1, user_id)  # Task ID doesn't match
        self.assertIsNone(task)

        task = Task.get_task_from_user(task_id + 1, user_id + 1)  # Neither Task ID nor User ID match
        self.assertIsNone(task)