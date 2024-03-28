from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from StudyHall.views import HomeView, RoomView, CreateRoom, UpdateRoom, DeleteRoom, DeleteMessage

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('room/<int:pk>/', RoomView.as_view(), name='room'),

    # sending resources
    # path('room/<int:room_id>/upload-resource/', UploadResource.as_view(), name='upload_resource'),

    # CRUD
    path('create-room/', CreateRoom.as_view(), name='create-room'),
    path('update-room/<int:pk>/', UpdateRoom.as_view(), name='update-room'),
    path('delete-room/<int:pk>/', DeleteRoom.as_view(), name='delete-room'),
    # delete a room message
    path('delete-message/<int:pk>/', DeleteMessage.as_view(), name='delete-message'),

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
