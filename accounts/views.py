from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from notes.models import Notes
from hall.models import Room, RoomMessage, Topic



class UserRegister(CreateView):
    """
    This class enables new users to register
    """
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        if user:
            login(self.request, user)

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class UserLogin(LoginView):
    """
    This class enables login functionality
    """
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been logged in successfully.') 
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

class UserLogout(RedirectView):
    """
    This class enables logout functionality
    """
    url = '/login' # where the user is redirected to after logged out

    def get(self, request, *args, **kwargs):
        """
        Enables users to logout
        """
        auth.logout(request) # callls Djangos built in logout function
        messages.success(request, 'You are now logged out')
        return super(UserLogout, self).get(request, *args, **kwargs)

class UserProfile(DetailView):
    model = User
    template_name = 'accounts/user-profile.html'
    paginate_by = 3
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        """
        Get additional data for the UserProfile class
        """
        context = super(UserProfile, self).get_context_data(**kwargs)
        user = self.object 
        # user_rooms = Room.objects.filter(Q(members=user) | Q(host=user))
        # topics = Topics.objects.filter(room__in=user_rooms).distinct() # gets the topics that the user is linked to
        notes = Notes.objects.filter(status='public') # gets users notes that are public

        # context['user_rooms'] = user_rooms
        # context['topics'] = topics
        context['notes'] = notes

        # recent_activities = RoomMessage.objects.filter(
        #     Q(room__in=user_rooms) & Q(sent_on__gte=timezone.now() - timezone.timedelta(days=7))
        # ).order_by('-sent_on')[:5]  # Get the room user is in and 5 most recent activities

        # context['recent_activities'] = recent_activities

        return context

class UpdateUser(TemplateView):
    model = User
    template_name = 'accounts/update-user.html'