from django.db import models
from django.urls import reverse

# Authentication
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm

class Token(models.Model):
    user = models.CharField(unique=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=100)

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

@receiver(post_save, sender=Playlist)
def set_permission(sender, instance, **kwargs):
    assign_perm('add_playlist', instance.user, instance)
    assign_perm('change_playlist', instance.user, instance)
    assign_perm('delete_playlist', instance.user, instance)
    assign_perm('view_playlist', instance.user, instance)