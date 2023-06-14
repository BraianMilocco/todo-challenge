# from django.test import TestCase
# from rest_framework.test import APIRequestFactory
# from rest_framework import status

# from .views import RegisterView
# from .serializers import UserSerializer

# from rest_framework.test import force_authenticate


# class RegisterViewTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()

#     def test_register(self):
#         url = '/register/'
#         request = self.factory.post(url, {'name': 'testuser', 'email': 'email@email.com', 
#                                           'password':'test234!Password'}, format='json')
#         response = view(request)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)