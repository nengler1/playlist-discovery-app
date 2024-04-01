from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from playlist_app.models import *
from playlist_app.forms import *

# Create your views here.
def index(request):
    playlist_list = Playlist.objects.all()
    print('Playlist list', playlist_list)
    print('Cover Image', playlist_list[0].cover.url)
    return render(request, 'playlist_app/index.html', {'playlist_list':playlist_list})

def create_playlist(request):
    form = PlaylistForm()
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.save()

    return render(request, 'playlist_app/create_playlist.html', {'form': form})
