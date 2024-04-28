from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django_quill.forms import QuillFormField
from django.shortcuts import render
from .models import Notes
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import NoteForm



# Create your views here.
class NoteView(LoginRequiredMixin, ListView):
    """
    This class handles the note view
    """
    model = Notes
    template_name = 'notes/notes.html'
    login_url = 'login'

    def get_queryset(self):
        """
        Search functionality for notes.
        Feat:
            Search by name and content
        """
        query = self.request.GET.get('q') 
        if query:
            return Notes.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(topic__name__icontains=query),
                user=self.request.user
            ).order_by('-updated_at')
        else:
            return Notes.objects.all()
    def get_context_data(self, **kwargs):
        """
        This method adds additional data
        """
        context = super().get_context_data(**kwargs)
        # notes = Notes.objects.filter(user=self.request.user)
        # context['notes'] = notes
        # context['notes'] = self.get_queryset()
        notes = context['object_list'].filter(user=self.request.user).order_by('updated_at')
        context['notes'] = notes
        context['status'] = [note.status for note in context['notes']]
        return context
    

class NoteDetail(LoginRequiredMixin, DetailView):
    """
    This class handles the view of a detailed note
    """
    model = Notes
    template_name = 'notes/detail-note.html' 


class CreateNote(LoginRequiredMixin, CreateView):
    """
    This class is responsible for creating new notes for logged in users
    """
    form_class = NoteForm
    template_name = 'notes/create-note.html'
    login_url = reverse_lazy('login') 
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        """"
        This method check if the form is valid, saves and creates a new task
        """
        form.instance.user = self.request.user

        return super(CreateNote, self).form_valid(form)
    
    def get_form(self, form_class=None):
        """
        Return an instance of the form to be used in this view.
        """
        form = super().get_form(form_class)
        form.fields['content'] = QuillFormField() # RichTex editor
        return form

class UpdateNote(LoginRequiredMixin, UpdateView):
    """
    This class is responsible for updating notes for logged in users
    """
    form_class = NoteForm
    template_name = 'notes/update-note.html'
    login_url = reverse_lazy('login') 
    success_url = reverse_lazy('notes')

    def get_queryset(self):
        """
        Returns the queryset for this view
        """
        slug = self.kwargs.get('slug')
        return Notes.objects.filter(slug=slug)
    
    def get_form(self, form_class=None):
        """
        Return an instance of the form to be used in this view.
        """
        form = super().get_form(form_class)
        form.fields['content'] = QuillFormField()
        return form

    def get_context_data(self, **kwargs):
        """
        Gets notes title to pass to update.html
        """
        context = super().get_context_data(**kwargs)
        context['note'] = self.get_object().title 
        return context

class DeleteNote(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete a task
    """
    model = Notes
    template_name = 'StudyHall/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('notes')

    def get_context_data(self, **kwargs):
        """
        Adds adds data contex for the object being deleted
        """
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object().title  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context
