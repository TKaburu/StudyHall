from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import RoomForm, TopicForm
from .models import Room, Topic, RoomMessage
from tasks.models import Tasks
from notes.models import Notes

class HomeView(ListView):
    """
    This class is responsible for the home page view
    """
    model = Room
    template_name = 'hall/home.html'
    context_object_name = 'rooms'
    paginate_by = 5
    
    def get_queryset(self):
        """
        Search functionality for the rooms.
        Feat:
            Search by name, description and host
        """
        query = self.request.GET.get('q')
        if query:
            return Room.objects.filter(
                Q(name__icontains=query) |
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
        context['topics'] = Topic.objects.all() # get all the topics
        context['room_chats'] = RoomMessage.objects.all().order_by('-sent_on')[:4] # only shows 4 latest activities

        # calculate the top 5 hosts by no of rooms created
        top_hosts = User.objects.annotate(num_rooms=Count('room')).filter(num_rooms__gt=0).order_by('-num_rooms')[:5]
        context['top_hosts'] = top_hosts
        if self.request.user.is_authenticated:
            context['tasks'] = Tasks.objects.filter(
                user=self.request.user,
                complete=False).order_by('due_date')[:5] # Tasks for the current user
            context['notes'] = Notes.objects.filter(
                user=self.request.user).order_by('updated_at')[:5]
        else:
            # context['tasks'] = None
            context['notes'] = None
        
        return context  

class AboutView(TemplateView):
    """
    This class handles the about page logic
    """
    template_name = 'hall/about.html'

class RoomView(DetailView):
    """
    This class is responsible for the detailed view of a room
    """
    model = Room
    template_name = 'hall/room-detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        """
        Gets additional data
        """
        context = super().get_context_data(**kwargs)
        room =  self.get_object() # gets a particular room 
        context['room_chats'] = RoomMessage.objects.filter(room=room).order_by('sent_on') # gets the messages for the particular room
        context['members'] = room.members.all()
        # context['resource'] = room.resource.all()
        # context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        room = self.get_object()
        if request.method == 'POST':
            # get the messages body to make sure an empty msg is not sent
            body = request.POST.get('body')
            if body.strip():
                RoomMessage.objects.create (
                    room=room, sender=request.user, body=request.POST.get('body')
                )
            room.members.add(request.user)
        return self.get(request, *args, **kwargs)

# # CRUD operations
class CreateRoom(LoginRequiredMixin, CreateView):
    """
    This class view creates a new room based on the Room model
    """
    model = Room
    form_class = RoomForm
    template_name = 'hall/create-room.html'
    login_url = reverse_lazy('login') # if user is not logged in they are redirected here
    success_url = reverse_lazy('home') # if user is logged in they are redirected here

    def get_context_data(self, **kwargs):
        """
        Gets additional data for the CreateRoom class
        """
        context = super(CreateRoom, self).get_context_data(**kwargs)
        topics = Topic.objects.all()
        context['topics'] = topics
        return context

    def form_valid(self, form):
        """
        This method checks if a fom is valid
        """

        room = form.save(commit=False)
        room.host = self.request.user
        room.save()
        return super().form_valid(form)

class UpdateRoom(LoginRequiredMixin, UpdateView):
    """
    This class enables logged in users to edit a room
    """
    model = Room
    form_class = RoomForm
    template_name = 'hall/update-room.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """
        Gets additional data for the UpdateRoom class
        """
        context = super(UpdateRoom, self).get_context_data(**kwargs)
        topics = Topic.objects.all()
        context['topics'] = topics
        return context
    
class DeleteRoom(LoginRequiredMixin, DeleteView):
    """
    This class enables logged in users to delete a room
    """
    model = Room
    template_name = 'hall/delete.html'
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
        context['obj'] = self.get_object().name  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
        return context

class DeleteMessage(LoginRequiredMixin, DeleteView):
     """
    This class enables logged in users to delete their room messages
     """
     model = RoomMessage
     template_name = 'hall/delete.html'
     login_url = reverse_lazy('login')
     # success_url = reverse_lazy('room')

     def get_success_url(self):
         """
         This method gets the primary key of the room to redirect to after 
         message is deleted
         """
         room_slug = self.object.room.slug
         return reverse_lazy('room', kwargs={'slug': room_slug})

     def get_context_data(self, **kwargs):
         """
         Adds the room title to the context
         """
         context = super().get_context_data(**kwargs)
         context['obj'] = self.get_object()  # obj since delete is dynamic it can delete anything: rooms, tasks, messages etc
         return context

class TopicView(ListView):
    """
    This clas list out all rooms of a specific topic
    """
    model = Topic
    template_name = "hall/topic.html"

    def get_queryset(self):
        """
        Get the queryset for the topics, annotating each topic with the count of rooms related to it
        """
        search_query = self.request.GET.get('q')
        if search_query:
            # Filter topics based on search query
            return Topic.objects.annotate(num_rooms=Count('room')).filter(
                Q(name__icontains=search_query)
            )
        else:
            return Topic.objects.annotate(num_rooms=Count('room'))

    def get_context_data(self, **kwargs):
        """
        This method gets additional data of the class
        """
        context = super().get_context_data(**kwargs)
        topics = self.get_queryset()
        context['topics'] = topics
        context['search_query'] = self.request.GET.get('q', '') 
        return context

class TopicDetail(ListView):
    model = Room
    template_name = 'hall/room-topic.html'
    form_class = RoomForm
    context_object_name = 'rooms'


    def get_queryset(self):
        topic_slug = self.kwargs.get('slug')
        topic = Topic.objects.get(slug=topic_slug)
        if topic:
            rooms = Room.objects.filter(topic=topic)
            search_query = self.request.GET.get('q')
            if search_query:
                rooms = rooms.filter(
                    Q(name__icontains=search_query) |
                    Q(description__icontains=search_query)
                )
            return rooms
        return Room.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.get(slug=self.kwargs.get('slug'))  # Retrieve the topic object
        context['topic_name'] = topic
        return context

class CreateTopic(LoginRequiredMixin, CreateView):
    """
    This class view creates a new room based on the Room model
    """
    model = Topic
    form_class = TopicForm
    template_name = 'hall/create-topic.html'
    login_url = reverse_lazy('login') # if user is not logged in they are redirected here
    success_url = reverse_lazy('topics') # if user is logged in they are redirected here

    def get_context_data(self, **kwargs):
        """
        Gets additional data for the CreateRoom class
        """
        context = super(CreateTopic, self).get_context_data(**kwargs)
        topics = Topic.objects.all()
        context['topics'] = topics
        return context

class UpdateTopic(LoginRequiredMixin, UpdateView):
    """
    This class handles updating a topic logic
    """
    model = Topic
    form_class = TopicForm
    template_name = 'hall/update-topic.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('topics')

    def get_context_data(self, **kwargs):
        """
        Gets additional data for the UpdateRoom class
        """
        context = super(UpdateTopic, self).get_context_data(**kwargs)
        topics = Topic.objects.all()
        context['topic'] = self.object
        return context
