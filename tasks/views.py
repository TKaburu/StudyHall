from datetime import date
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
# from .forms import TaskForm
from .models import Tasks
from .forms import TaskForm



# Create your views here.


class TasksView(LoginRequiredMixin, ListView):
    """
    This class is responsible for the task dashboard view
    """
    model = Tasks
    template_name = 'tasks/tasks.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        """
        Search functionality for tasks.
        Feat:
            Search by name, description and host
        """
        filter_set = self.request.GET.get('filter', 'all') # for the different filters
        query = self.request.GET.get('q')        
        if query:
            tasks = Tasks.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
                user=self.request.user
            )
        else:
            tasks = Tasks.objects.all()

        if filter_set == 'complete':
            tasks = tasks.filter(complete=True)
        elif filter_set == 'incomplete':
            tasks = tasks.filter(complete=False)
        elif filter_set == 'overdue':
            tasks = tasks.filter(due_date__lt=date.today(), complete=False)

        return tasks.order_by('due_date')
    
    def get_context_data(self, **kwargs):
        """
        This method adds additional data
        """
        context = super().get_context_data(**kwargs)
        tasks = context['object_list'].filter(user=self.request.user).order_by('due_date') # gets the tasks for specific logged in user
        # context['incomplete_task_count'] = Tasks.objects.filter(complete=False).count()
        if self.request.user.is_authenticated:
            # context['tasks'] = Tasks.objects.filter(user=self.request.user).order_by('due_date')
            context['tasks'] = tasks
        # context['tasks'] = tasks
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    """
    This class handles the detail view of a task logic
    """
    model = Tasks
    template_name = 'tasks/task-detail.html'
    login_url = reverse_lazy('login')

class CreateTask(LoginRequiredMixin, CreateView):
    """
    This class is responsible for creating new tasks for logged in users
    """
    form_class = TaskForm
    template_name = 'tasks/create-task.html'
    login_url = reverse_lazy('login') 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """
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
        slug = self.kwargs.get('slug')
        return Tasks.objects.filter(slug=slug)

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
    template_name = 'hall/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        """
        Adds adds data contex for the object being deleted
        """
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object().title  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context
