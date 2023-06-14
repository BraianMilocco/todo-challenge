from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from login.models import MyUser
from ..models import Task
from ..serializers import TaskSerializer
from ..views import TasksView, TaskView, TaskComplete, get_task


class TasksViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.url = reverse('tasks')
        self.view = TasksView.as_view()

    def test_post_valid_data(self):
        request = self.factory.post(self.url, data={
            'title': 'Test Task',
            'description': 'This is a test task'
        })
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)

    def test_post_invalid_data(self):
        request = self.factory.post(self.url, data={})
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_get(self):
        Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user=self.user
        )

        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TaskViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user=self.user
        )
        self.url = reverse('task', kwargs={'task_id': self.task.id})
        self.view = TaskView.as_view()

    def test_get_task_not_found(self):
        url = reverse('task', kwargs={'task_id': self.task.id + 1})

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id + 1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.id)

    def test_put(self):
        request = self.factory.put(self.url, data={'title': 'Updated Task'})
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_delete(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'task deleted')


class TaskCompleteTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user=self.user
        )
        self.url = reverse('task_complete', kwargs={'task_id': self.task.id})
        self.view = TaskComplete.as_view()

    def test_complete_task_not_found(self):
        url = reverse('task_complete', kwargs={'task_id': self.task.id + 1})

        request = self.factory.put(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id + 1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_complete_task(self):
        request = self.factory.put(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, task_id=self.task.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])


class HelperFunctionTest(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(name='testuser', email="testemail@email", password="t!1@ASDest" )
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            user=self.user
        )

    def test_get_task(self):
        task = get_task(self.task.id, self.user.id)
        self.assertEqual(task, self.task)

        task = get_task(self.task.id, self.user.id + 1)  # User ID doesn't match
        self.assertIsNone(task)

        task = get_task(self.task.id + 1, self.user.id)  # Task ID doesn't match
        self.assertIsNone(task)

        task = get_task(self.task.id + 1, self.user.id + 1)  # Neither Task ID nor User ID match
        self.assertIsNone(task)
