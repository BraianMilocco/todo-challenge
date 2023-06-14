from django.db import models
from django.db.models import Q
## add logger
import logging
logger = logging.getLogger(__name__)

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    delete = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('login.MyUser', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    @staticmethod
    def create_dynamic_filter(filters, **kwargs):
        for key, value in kwargs.items():
            if key == 'completed':
                filters &= Q(completed=value)
            elif key == 'title':
                filters &= Q(title__icontains=value)
            elif key == 'description':
                filters &= Q(description__icontains=value)
            elif key == 'created_at':
                crated_at = value.split('-')
                if len(crated_at) == 1:
                    continue
                filters &= Q(created_at__year=crated_at[0], created_at__month=crated_at[1], created_at__day=crated_at[2])
        return filters

    @classmethod
    def get_all_from_user(cls, user_id, **kwargs):
        filters = Q(user_id=user_id, delete=False)
        filters = cls.create_dynamic_filter(filters, **kwargs)
        return cls.objects.filter(filters)

    @classmethod
    def get_task_from_user(cls, task_id, user_id):
        try:
            return cls.objects.get(id=task_id, user_id=user_id, delete=False)
        except cls.DoesNotExist:
            logger.error(f'Task with id {task_id} does not exist, is deleted, or does not belong to user {user_id}')
            return None
