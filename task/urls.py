from django.urls import path
from .views import TasksView, TaskView, TaskComplete


urlpatterns = [
    path('task/', TasksView.as_view(), name="tasks"),
    path('task/<int:task_id>/', TaskView.as_view(), name="task"),
    path('task/<int:task_id>/complete/', TaskComplete.as_view(), name="task_complete"),
]
