from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic
from django.contrib import messages
from playlist_app.models import *
from playlist_app.forms import *

# Authentication
from django.contrib.auth.decorators import login_required
from .decorators import *

# API
import spotipy
from .credentials import *
from rest_framework.decorators import api_view
from spotipy.oauth2 import SpotifyOAuth

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
        print('\nPOST:', request.POST)
        print('\nFILES:', request.FILES, '\n')
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            print('PLAYLIST:', playlist)
            playlist.save()
            # Using save_m2m to save from Many to Many
            form.save_m2m()

            return redirect('index')
    return render(request, 'playlist_app/create_playlist.html', {'form': form})

@login_required(login_url='login')
@user_is_owner()
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

@login_required(login_url='login')
@user_is_owner()
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

def playlist_detail(request, pk):
    playlist = Playlist.objects.get(id=pk)
    return render(request, "playlist_app/playlist_detail.html", 
                  {'playlist':playlist})

def spotify_oauth():
    # Using spotipy to create an OAuth object
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        state=STATE,
        scope='user-top-read',
        show_dialog=True,
    )

def spotify_login(request):
    # Getting the url for the OAuth
    url = spotify_oauth().get_authorize_url()
    # Redirecting user to Spotify Login page
    return HttpResponseRedirect(url)


def spotify_redirect(request):
    # Getting auth code from GET request dictionary
    code = request.GET.get("code")
    #print("\nCODE:", code, "\n")

    # Requesting access token using auth code from get_access_token
    token_info = spotify_oauth().get_access_token(code)

    # Getting that access token
    access_token = token_info["access_token"]
    # Storing the access token in our current session (secure way)
    request.session["access_token"] = access_token

    # Redirecting user to the users top artist page
    return HttpResponseRedirect("/spotify/top_artists/")

# Wrapping the function into a Function Based view ensuring we receive GET request
# From REST Framework
@api_view(['GET'])
def get_top_artists(request):
    if request.method == 'GET':

        # Getting our secured access token from the session in request (dictionary)
        # This is saved locally as .cache file
        access_token = request.session["access_token"]
        print('\nACCESS TOKEN:', access_token)

        # Handle missing access token error
        if not access_token:
            error = "Access token is missing"
            return HttpResponseBadRequest(error)

        # Creating a Spotipy client with our access token
        sp = spotipy.Spotify(auth=access_token)

        # Getting the user's profile information
        response = sp.me()
        username = ""
        # Checking to see if response was successful or not
        if response is not None:
            print("\nAccess Token is valid.")

            username = response["display_name"]
            print("CURRENT USER:", username)
        else:
            print("\nAccess Token is invalid or has expired.\n")

        # Our GET request to the Spotify API for the JSON Object
        response = sp.current_user_top_artists(
            limit=10,
            offset=0,
            time_range="long_term"
        )

        # Extracting top artists from JSON (python dictionary)
        top_artists = response["items"]
        artists = []
        # iterating through extracted top artists by name, genres, and their image covers
        for artist in top_artists:
            artist_info = {
                "name": artist['name'],
                "genres": artist['genres'],
                "image": artist['images'][0]['url'],
            }
            artists.append(artist_info)

        print("\nLIST OF ARTISTS:", artists, "\n\n")

        # returing the request of artists list to the top_artists html file
        # (as well as the user's username)
        return render(request, 'playlist_app/top_artists.html',
                      {'artists':artists, 'username':username})
    
    # If we didn't get the GET request, we return an error message
    else:
        error = "An error occurred with GET request. Unsupported request method used."
        return HttpResponseBadRequest(error)
