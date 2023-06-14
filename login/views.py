from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
import logging

logger = logging.getLogger(__name__)


# view for registering users
class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as errors:
            logger.info(f'Error creating user: {errors}')
            return Response({"message": "verify the data sent"}, status=400)
        serializer.save()
        return Response(serializer.data)
    def get(self, request):
        return Response({"message": "Hello, world!"})
