# from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Room, Topics

# Create your views here.


class HomeView(ListView):
    """
    This class is responsible for the home page view
    """
    model = Room
    template_name = 'StudyHall/home.html'
    context_object_name = 'rooms'
    
    def get_queryset(self):
        """
        Search functionality for the rooms.
        Feat:
            Search by name, description and host
        """
        query = self.request.GET.get('q')
        if query:
            return Room.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(host__username__icontains=query) |
                Q(topic__name__icontains=query)
            )
        else:
            return Room.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_count'] = Room.objects.count() # Calculate how many rooms ther are 
        context['topics'] = Topics.objects.all() # get all the topics

        # calculate the top 10 hosts by no of rooms created
        top_host = 

        return context  


class RoomView(DetailView):
    """
    This class is responsible for the detailed view of a room
    """
    model = Room
    template_name = 'StudyHall/room.html'
    context_object_name = 'room'

    def get_object(self, queryset=None):
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)
     

# CRUD operations
class CreateRoom(CreateView):
    """
    This class view creates a new room based on the Room model
    """
    model = Room
    fields = ['title', 'host', 'description', 'topic']
    template_name = 'StudyHall/create-room.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Checks if the form passed is valid and saves the data
        """
        form.instance.host = self.request.user

        return super().form_valid(form)

class UpdateRoom(UpdateView):
    model = Room
    fields = ['title', 'host', 'description', 'topic']
    template_name = 'studyHall/update-room.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)
    
class DeleteRoom(DeleteView):
    model = Room
    template_name = 'studyHall/delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)