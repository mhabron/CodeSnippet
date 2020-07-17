from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django import forms

class Location(models.Model):
    name = models.CharField(max_length=25)
    curated = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class Post(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_logo = models.ImageField(upload_to='static/logos', blank=True, default='https://brand.gmu.edu/wp-content/uploads/assets/primarylogo/PC/GMURGB.jpg')
    address = models.CharField(max_length=200, default='4400 University Dr, Fairfax, VA 22030')
    created_date = models.DateTimeField(default=timezone.now)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # def __init__(self, *args, **kwargs):
    #     host = User.objects.first() # TODO: REMOVE
    #     super().__init__(*args, **kwargs)

    def __str__(self):
        return self.title
