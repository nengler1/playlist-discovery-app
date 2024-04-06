from django import forms
from .models import *

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', 'artists', 'genres', 'cover',)