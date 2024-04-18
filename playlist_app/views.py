from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
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
from rest_framework.views import APIView
from rest_framework import status, response
from requests import Request, post
from .credentials import *
from .extras import *

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

class AuthenticationURL(APIView):
    def get(self, request, format=None):
        scopes = "user-library-read"
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope':scopes,
            'response_type':'code',
            'redirect_uri': REDIRECT_URI,
            'client_id':CLIENT_ID
        }).prepare().url

        return HttpResponseRedirect(url)
    
def spotify_redirect(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return error
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code':code,
        'redirect_uri':REDIRECT_URI,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    authKey = request.session.session_key
    if not request.session.exists(authKey):
        request.session.create()
        authKey = request.session.session_key

    create_or_update_tokens(
        session_id = authKey,
        access_token = access_token,
        refresh_token = refresh_token,
        expires_in = expires_in,
        token_type = token_type
    )

    # Create a redirect url
    redirect_url = ''
    return HttpResponseRedirect(redirect_url)

# Checking whether the user has been authenticated by spotify
class CheckAuthentication(APIView):
    def get(self, request, format=None):
        key = self.request.session.session_key

        if not self.request.session.exits(key):
            self.request.session.create()
            key = self.request.session.session_key

        auth_status = is_spotify_authenticated(key)

        if auth_status:
            redirect_url = ''
            return HttpResponseRedirect(redirect_url)
        else:
            redirect_url = ''
            return HttpResponseRedirect(redirect_url)