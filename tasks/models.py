from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Overide the save method so as to use the slug for the url
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tasks, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        This method enables the slug to be used in the url
        """
        return reverse('task', kwargs={'slug': self.slug})
    

    def __str__(self):
        return self.title
    