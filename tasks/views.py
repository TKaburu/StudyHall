from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
# from .forms import TaskForm
from .models import Tasks
from .forms import TaskForm



# Create your views here.


class TasksView(ListView):
    """
    This class is responsible for the task dashboard view
    """
    model = Tasks
    template_name = 'tasks/task-dashboard.html'

    def get_context_data(self, **kwargs):
        """
        This method adds additional data
        """
        context = super().get_context_data(**kwargs)
        tasks = context['object_list'].filter(user=self.request.user) # gets the tasks for specific logged in user
        context['tasks'] = tasks
        context['count'] = tasks.filter(complete=False).count() # Counts the number of incomplete tasks
        return context

class CreateTask(LoginRequiredMixin, CreateView):
    """
    This class is responsible for creating new tasks for logged in users
    """
    form_class = TaskForm
    template_name = 'tasks/create-task.html'
    login_url = reverse_lazy('login') 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """"
        This method check if the form is valid, saves and creates a new task
        """
        form.instance.user = self.request.user

        return super(CreateTask, self).form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    """
    This class is responsible for updating tasks for logged in users
    """
    form_class = TaskForm
    template_name = 'tasks/update-task.html'
    login_url = reverse_lazy('login') 
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        """
        Returns the queryset for this view
        """
        pk = self.kwargs.get('pk')
        return Tasks.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        """
        Gets task title to pass to update.html
        """
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object().title 
        return context

class DeleteTask(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete a task
    """
    model = Tasks
    template_name = 'studyHall/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        """
        Adds adds data contex for the object being deleted
        """
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object().title  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context
