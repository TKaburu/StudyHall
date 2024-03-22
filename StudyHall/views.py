from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Room, Topics, RoomChats

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
            return Room.objects.all().order_by('-updated_on', '-created_on')
        
    def get_context_data(self, **kwargs):
        """
        Gets different data such as room count, topics, messages etc
        """
        context = super().get_context_data(**kwargs)
        context['room_count'] = Room.objects.count() # Calculate how many rooms ther are 
        context['topics'] = Topics.objects.all() # get all the topics

        # calculate the top 5 hosts by no of rooms created
        top_hosts = User.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[:5]
        context['top_hosts'] = top_hosts
        return context  

class RoomView(DetailView):
    """
    This class is responsible for the detailed view of a room
    """
    model = Room
    template_name = 'StudyHall/room-detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        """
        Gets room messages
        """
        context = super().get_context_data(**kwargs)
        context['room_chats'] = RoomChats.objects.all()
        return context


    def get_object(self, queryset=None):
        """
        Gets the name/title of the room
        """
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)
     

# CRUD operations
class CreateRoom(LoginRequiredMixin, CreateView):
    """
    This class view creates a new room based on the Room model
    """
    model = Room
    fields = ['title', 'host', 'description', 'topic']
    template_name = 'StudyHall/create-room.html'
    login_url = reverse_lazy('login') # if user is not logged in they are redirected here
    success_url = reverse_lazy('home') # if user is logged in they are redirected here

    def form_valid(self, form):
        """
        Checks if the form passed is valid and saves the data
        """
        form.instance.host = self.request.user

        return super().form_valid(form)

class UpdateRoom(LoginRequiredMixin, UpdateView):
    """
    This class enables logged in users to edit a room
    """
    model = Room
    fields = ['title', 'host', 'description', 'topic']
    template_name = 'studyHall/update-room.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Gets the name/title of the room
        """
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)
    
class DeleteRoom(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete a room
    """
    model = Room
    template_name = 'studyHall/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        """
        Gets the name/title of the room
        """
        room_title = self.kwargs['room_title']
        return Room.objects.get(title=room_title)

