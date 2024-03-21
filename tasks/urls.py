from django.urls import path
from .views import NewTask, TasksView

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('create-task/', NewTask.as_view(), name='create-task'),

]