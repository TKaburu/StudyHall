from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Topic(models.Model):
    """
    This class defines a topic
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        """
        Overide the save method so as to use the slug for the url
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Topic, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        This method enables the slug to be used in the url
        """
        return reverse('topic', kwargs={'slug': self.slug})

    def __str__(self):
        """
        String representation of the class Topic
        """
        return self.name

    
class Room(models.Model):
    """
    This class defines a room
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True)
    room_chats = models.ManyToManyField('RoomMessage', related_name='room_messages', blank=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Overide the save method so as to use the slug for the url
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        This method enables the slug to be used in the url
        """
        return reverse('room', kwargs={'slug': self.slug})
    
    class meta:
        ordering = ['-updated_on', '-created_on']
        
    # String representation
    def __str__(self):
        """
        String representation of the class Room
        """
        return self.name


class RoomMessage(models.Model):
    """
    This class defines a room message
    """
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    sent_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        """
        String representation for the RoomChats model
        """
        return f"Comment by {self.sender.username} on {self.room}"