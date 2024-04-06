from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from playlist_app.models import *
from playlist_app.forms import *

# Create your views here.
def index(request):
    playlist_list = Playlist.objects.all()
    print('Playlist list', playlist_list)
    return render(request, 'playlist_app/index.html', {'playlist_list':playlist_list})

def create_playlist(request):
    form = PlaylistForm()
    if request.method == 'POST':
        print("FILES", request.FILES)
        print("POST", request.POST)
        form = PlaylistForm(request.POST, request.FILES)
        print(form.__dict__)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.save()
            form.save_m2m()

            return redirect('index')
    return render(request, 'playlist_app/create_playlist.html', {'form': form})

def update_playlist(request, pk):
    playlist = Playlist.objects.get(id=pk)

    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            saved_playlist = form.save(commit=False)
            saved_playlist.save()
            form.save_m2m()

            return redirect('playlist-detail', pk)
    else:
        form = PlaylistForm(instance=playlist)

    return render(request, 'playlist_app/update_playlist.html', 
                  {'form': form, 'pk':pk})

def delete_playlist(request, pk):
    playlist = Playlist.objects.get(id=pk)
    print("PLAYLIST TO DELETE", playlist)

    if request.method == 'POST':
        playlist.delete()
        return redirect('index')
    
    return render(request, 'playlist_app/delete_playlist.html', 
                  {'playlist': playlist, 'pk':pk})

class PlaylistListView(generic.ListView):
    model = Playlist
    context_object_name = 'playlist_list'
    template_name = 'playlist_app/playlist_list.html'

class PlaylistDetailView(generic.DetailView):
    model = Playlist
    template_name = 'playlist_app/playlist_detail.html'