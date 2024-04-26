from django.db import models
from django.urls import reverse

# Authentication
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Playlist(models.Model):
    title = models.CharField(max_length=200, blank=False)
    artists = models.ManyToManyField(Artist, default=None)
    genres = models.ManyToManyField(Genre, default=None)
    cover = models.ImageField(default='playlist_default.png')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.pk)])
