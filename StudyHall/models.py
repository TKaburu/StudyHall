from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Room(models.Model):
    """
    This class defines a room
    """
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey('Topics', on_delete=models.SET_NULL, null=True)
    room_chats = models.ManyToManyField('RoomChats', related_name='room_chats', blank=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    updated_on = models.DateTimeField(auto_now=True) # Every time there is activity in the room
    created_on = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['-updated_on', '-created_on']

    # String representation
    def __str__(self):
        """
        String representation of the class Room
        """
        return self.title
    
class Topics(models.Model):
    """
    This class define a topic
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation of the class Topic
        """
        return self.name
    
# Room comments/chats
class RoomChats(models.Model):
    """
    This class is responsible for chats/comments sent to a room
    """
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    sent_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f"Comment by {self.sender.username} on {self.room.title}"
    
# class Resources(models.Model):
#     """
#     This class defines a resource (e.g., link, PDF, video, picture) uploaded by a user in a room
#     """
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     file = models.FileField(upload_to='resources/')
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title