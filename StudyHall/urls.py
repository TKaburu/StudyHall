from django.urls import path
from StudyHall.views import HomeView, RoomView, CreateRoom, UpdateRoom, DeleteRoom

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('room/<str:room_title>/', RoomView.as_view(), name='room'),

    # CRUD
    path('create-room/', CreateRoom.as_view(), name='create-room'),
    path('update-room/<str:room_title>', UpdateRoom.as_view(), name='update-room'),
    path('delete-room/<str:room_title>', DeleteRoom.as_view(), name='delete-room'),
]
