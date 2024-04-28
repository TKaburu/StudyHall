from django.urls import path
from .views import NoteView, NoteDetail, CreateNote, UpdateNote, DeleteNote


urlpatterns = [
    path('notes/', NoteView.as_view(), name='notes'),
    path('notes/<slug:slug>/', NoteDetail.as_view(), name='note'),

    # Create, Update and Delete
    path('create-note/', CreateNote.as_view(), name='create-note'),
    path('update-note/<slug:slug>/', UpdateNote.as_view(), name='update-note'),
    path('delete-note/<slug:slug>/', DeleteNote.as_view(), name='delete-note'),

]