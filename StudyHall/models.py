from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Room(models.Model):
    title = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey('Topics', on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    updated_on = models.DateTimeField(auto_now=True) # Every time there is activity in the room
    created_on = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['-updated_on', '-created_on']

    # String representation
    def __str__(self):
        return self.title
    
class Topics(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    