from django.contrib.auth.models import User
from django.db import models
from django_quill.fields import QuillField
from django.urls import reverse
from django.utils.text import slugify
from hall.models import Topic


# Create your models here.

class Notes(models.Model):
    """
    This class describes a note
    """

    # check if a note is private or public
    STATUS = (
        ('private', 'Private'),
        ('public', 'Public'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = QuillField()
    status = models.CharField(max_length=200, choices=STATUS, default='private')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['-updated_on']

    def save(self, *args, **kwargs):
        """
        Overide the save method so as to use the slug for the url
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Notes, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        This method enables the slug to be used in the url
        """
        return reverse('note', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
