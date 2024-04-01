from django.db import models
from django.urls import reverse

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
    artists = models.ManyToManyField(Artist)
    genres = models.ManyToManyField(Genre)
    cover = models.ImageField(upload_to='static/uploads/', null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.pk)])