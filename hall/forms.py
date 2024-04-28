from django import forms
from .models import Room, Topic

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'topic']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']