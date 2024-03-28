from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# from .forms import UploadResourceForm
from .models import Room, Topics, RoomChats
from tasks.models import Tasks

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
        context['room_chats'] = RoomChats.objects.all()

        # calculate the top 5 hosts by no of rooms created
        top_hosts = User.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[:5]
        context['top_hosts'] = top_hosts
        if self.request.user.is_authenticated:
            context['tasks'] = Tasks.objects.filter(user=self.request.user) # Tasks for the current user
        else:
            context['tasks'] = None


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
        Gets additional data
        """
        context = super().get_context_data(**kwargs)
        room =  self.get_object() # gets a particular room 
        context['room_chats'] = RoomChats.objects.filter(room=room).order_by('sent_on') # gets the messages for the particular room
        context['members'] = room.members.all()
        # context['resource'] = room.resource.all()
        # context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        room = self.get_object()
        if request.method == 'POST':
            RoomChats.objects.create (
                room=room, sender=request.user, body=request.POST.get('body')
            )
            room.members.add(request.user)
        return self.get(request, *args, **kwargs)
     

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

    # def get_object(self, queryset=None):
    #     """
    #     Gets the name/title of the room
    #     """
    #     room_title = self.kwargs['room_title']
    #     return Room.objects.get(title=room_title)
    
class DeleteRoom(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete a room
    """
    model = Room
    template_name = 'studyHall/delete.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    # def get_object(self, queryset=None):
    #     """
    #     Gets the room object based on the provided pk
    #     """
    #     obj = super().get_object(queryset=queryset)
    #     if obj is None:
    #         raise Http404("Room does not exist")
    #     return obj

    def delete(self, request, *args, **kwargs):
        # Get the room object
        room = self.get_object()
        
        # Delete the associated room chats
        room.room_chats.all().delete()
        
        # Delete the room
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds the room title to the context
        """
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object().title  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context


# class UploadResource(FormView):
#     template_name = 'upload_resource.html'
#     form_class = UploadResourceForm

#     def form_valid(self, form):
#         room_id = self.kwargs['room_id']
#         room = Room.objects.get(id=room_id)
#         resource = form.save(commit=False)
#         resource.room = room
#         resource.sender = self.request.user
#         resource.save()
#         return redirect('room', room_id=room_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['room_id'] = self.kwargs['room_id']
#         return context

class DeleteMessage(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete their room messages
    """
    model = RoomChats
    template_name = 'studyHall/delete.html'
    login_url = reverse_lazy('login')
    # success_url = reverse_lazy('room')

    def get_success_url(self):
        """
        This method gets the primary key of the room to redirect to after 
        message is deleted
        """
        room_pk = self.object.room.pk  
        return reverse_lazy('room', kwargs={'pk': room_pk})

    def get_context_data(self, **kwargs):
        """
        Adds the room title to the context
        """
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object()  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context



   