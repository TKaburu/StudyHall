from django.urls import path
from .views import CreateTask, TasksView, TaskDetail, UpdateTask, DeleteTask

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
    path('tasks/<slug:slug>/', TaskDetail.as_view(), name='task'),

    # Create, Update and Delete
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('update-task/<slug:slug>/', UpdateTask.as_view(), name='update-task'),
    path('delete-task/<slug:slug>/', DeleteTask.as_view(), name='delete-task'),

]