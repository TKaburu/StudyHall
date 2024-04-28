from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('room/<slug:slug>/', views.RoomView.as_view(), name='room'),

    path('topics/', views.TopicView.as_view(), name='topics'),
    path('topic/<slug:slug>/', views.TopicDetail.as_view(), name='topic-detail'),

    path('create-room/', views.CreateRoom.as_view(), name='create-room'),
    path('update-room/<slug:slug>/', views.UpdateRoom.as_view(), name='update-room'),
    path('delete-room/<slug:slug>/', views.DeleteRoom.as_view(), name='delete-room'),
    # delete a room message
    path('delete-message/<int:pk>/', views.DeleteMessage.as_view(), name='delete-message'),

    # CRUD for Topics
    path('create-topic/', views.CreateTopic.as_view(), name='create-topic'),
    path('update-topic/<slug:slug>/', views.UpdateTopic.as_view(), name='update-topic'),
]