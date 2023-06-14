from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import MyUser
from ..serializers import UserSerializer

class RegisterViewTest(APITestCase):
    def test_register_user(self):
        url = reverse('sign_up')
        data = {
            'name': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MyUser.objects.count(), 1)

        user = MyUser.objects.first()
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)