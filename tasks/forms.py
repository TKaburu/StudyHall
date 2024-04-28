from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'due_date', 'complete']
        # widget for calendar pop up for due date
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }