from django.test import TestCase
from login.models import MyUser
from ..models import Task
from ..serializers import TaskSerializer

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'user_id': self.user.id
        }
        self.serializer = TaskSerializer(data=self.task_data)

    def test_create_task(self):
        self.assertTrue(self.serializer.is_valid())
        task = self.serializer.save()

        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'This is a test task')
        self.assertFalse(task.delete)
        self.assertFalse(task.completed)
        self.assertEqual(task.user_id, self.user.id)

    def test_delete_task(self):
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user_id=self.user.id
        )
        updated_task = TaskSerializer.delete(task)
        self.assertTrue(updated_task.delete)

    def test_complete_task(self):
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user_id=self.user.id
        )
        updated_task = TaskSerializer.complete(task)
        self.assertTrue(updated_task.completed)