from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
# from .forms import TaskForm
from .models import Tasks



# Create your views here.


class TasksView(ListView):
    """
    This class is responsible for the task dashboard view
    """
    model = Tasks
    template_name = 'tasks/task-dashboard.html'

    def get_context_data(self, **kwargs):
        """
        This method filters tasks to a particular signed in user
        """
        contex = super().get_context_data(**kwargs)
        contex['tasks'] = contex['tasks'].filter(user=self.request.user)
        contex['count'] = contex['tasks'].filter(complete=False).count()
        return contex

class NewTask(CreateView):
    """
    This class is responsible for creating new tasks
    """
    model = Tasks
    template_name = 'tasks/create-task.html'
    fields = ['task', 'description', 'due_date', 'complete']
    widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
    success_url = reverse_lazy('tasks')

    # def get_form_kwargs(self):
    #     """
    #     Pass the user instance to the form when it is instantiated
    #     """
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    def form_valid(self, form):
        """"
        This method check if the form is valid, saves and creates a new task
        """
        form.instance.user = self.request.user

        return super(NewTask, self).form_valid(form)