from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from playlist_app.models import *
from playlist_app.forms import *

# Authentication
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from guardian.shortcuts import assign_perm, get_objects_for_user
from guardian.decorators import permission_required_or_403

# API
import spotipy
from .credentials import *
from rest_framework.decorators import api_view
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# Create your views here.
def index(request):
    playlist_list = Playlist.objects.all()
    #print('Playlist list', playlist_list)
    return render(request, 'playlist_app/index.html', {'playlist_list':playlist_list})

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print("REQUEST!", request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            playlist_user = Playlist.objects.create(user=user,)
            playlist_user.save()

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    return render(request, 'registration/register.html', {'form':form})
            
@login_required(login_url='login')
def create_playlist(request):
    form = PlaylistForm()
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
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

@login_required(login_url='login')
def playlist_detail(request, pk):
    playlist = Playlist.objects.get(id=pk)
    return render(request, "playlist_app/playlist_detail.html", 
                  {'playlist':playlist})

def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )

    print("\nSP_OAUTH OBJECT: ", sp_oauth, "\n")

    url = sp_oauth.get_authorize_url()
    print("URL:",url)

    return HttpResponseRedirect(url)

def spotify_redirect(request):
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )

    code = request.GET.get("code")

    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    request.session["access_token"] = access_token

    return HttpResponseRedirect("/spotify/top_artists/")

@api_view(['GET'])
def get_top_artists(request):
    if request.method == 'GET':
        access_token = request.session.get("access_token")
        print('\nACCESS TOKEN:', access_token, '\n')
    
        sp = spotipy.Spotify(auth=access_token)

        response = sp.me()

        if response is not None:
            print("\nAccess Token is valid.")
        else:
            print("\nAccess Token is invalid or has expired.\n")
        
        username = sp.me()['display_name']

        response = sp.current_user_top_artists(
            limit=15,
            offset=0,
            time_range="long_term"
        )

        top_artists = response["items"]

        artists = []
        for artist in top_artists:
            artist_info = {
                "name": artist['name'],
                "genres": artist['genres'],
                "image": artist['images'][0]['url'],
            }
            artists.append(artist_info)

        #print("\nTOP ARTISTS:", top_artists)
        print("CURRENT USER:", username)
        print("\n\nLIST OF ARTISTS:", artists, "\n\n")
        

        return render(request, 'playlist_app/top_artists.html',
                      {'artists':artists, 'username':username})
    
    else:
        error = "An error occurred with GET"
        return error
