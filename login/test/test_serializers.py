from django.test import TestCase
from ..serializers import UserSerializer

class UserSerializerTest(TestCase):
    def test_create_user(self):
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpassword',
        }

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertTrue(user.check_password(data['password']))