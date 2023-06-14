from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from .models import Task
import logging

logger = logging.getLogger(__name__)

# view for registering users
class TasksView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a task"""
        try:
            data = {
                'title': request.data.get('title', None),
                'description': request.data.get('description', None),
                'user_id': request.user.id
            }
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except Exception as errors:
            logger.info(f'Error creating task: {errors}')
            return Response({"message": "verify the data sent"}, status=400)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        """Get all tasks non deleted from user
            Optional query_params: title, description, completed, created_at"""
        params = request.query_params.dict()
        tasks = Task.get_all_from_user(request.user.id, **params)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


def get_task(task_id, user_id):
    """Helper function to get a task from user"""
    task = Task.get_task_from_user(task_id, user_id)
    if not task:
        return None
    return task


class TaskView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_task_not_found_response(self):
        return Response({"message": "Task not found"}, status=404)

    def get(self, request, task_id):
        """Get a task by id"""
        task = get_task(task_id, request.user.id)
        if not task:
            return self.get_task_not_found_response()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, task_id):
        """Update a task (partial update)
            Valid fields: Title, description"""
        task = get_task(task_id, request.user.id)
        if not task:
            return self.get_task_not_found_response()
        try:
            serializer = TaskSerializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
        except Exception as errors:
            logger.info(f'Error updating task: {errors}')
            return Response({"message": "verify the data sent"}, status=400)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, task_id):
        """"Delete a task (logical delete)"""
        task = get_task(task_id, request.user.id)
        if not task:
            return self.get_task_not_found_response()
        try:
            TaskSerializer.delete(task)
        except Exception as errors:
            logger.error(f'Error deleting task: {errors}')
            return Response({"message": "Internal Error"}, status=500)
        return Response({"message": "task deleted"})

class TaskComplete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        """Complete or uncomplete a task"""
        task = get_task(task_id, request.user.id)
        if not task:
            return Response({"message": "Task not found"}, status=404)
        try:
            instance = TaskSerializer.complete(task)
            serializer = TaskSerializer(instance)
        except Exception as errors:
            logger.info(f'Error completing task: {errors}')
            return Response({"message": "Internal Error"}, status=500)
        return Response(serializer.data)