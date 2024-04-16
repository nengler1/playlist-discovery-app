from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', 'artists', 'genres', 'cover',)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']