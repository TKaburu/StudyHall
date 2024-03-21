from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from .forms import RegisterForm

# Create your views here.

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

# class UserProfile()
