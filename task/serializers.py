from rest_framework import serializers
from .models import Task
from login.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Task
        fields = ["id", "title", "description", "delete", "user_id", "completed", "created_at"]
        read_only_fields = ["id", "delete", "completed", "created_at", "user_id"]

    def create(self, validated_data):
        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            user_id=validated_data['user_id']
        )

        task.save()
        return task
    
    @classmethod
    def delete(cls, instance):
        instance.delete = True
        instance.save()
        return instance
    
    @classmethod
    def complete(cls, instance):
        instance.completed = not instance.completed
        instance.save()
        return instance