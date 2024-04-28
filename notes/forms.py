from django import forms
from django_quill.fields import QuillFormField
from .models import Notes

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'topic', 'content', 'status']
        # adding quil editor
        widgets = {
            'content': QuillFormField(),
        }