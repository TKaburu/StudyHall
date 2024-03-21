from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['task', 'description', 'due_date', 'complete']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }