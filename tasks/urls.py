from django.urls import path
from .views import CreateTask, TasksView, UpdateTask, DeleteTask

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),

    # Create, Update and Delete
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('update-task/<int:pk>/', UpdateTask.as_view(), name='update-task'),
    path('delete-task/<int:pk>/', DeleteTask.as_view(), name='delete-task'),

]