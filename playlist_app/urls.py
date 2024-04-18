from django.urls import path, include
from . import views


urlpatterns = [
#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
    path('', views.index, name='index'),
    path('playlists/', views.PlaylistListView.as_view(), name='playlists'),
    path('playlist/<int:pk>', views.playlist_detail, name='playlist-detail'),
    path('create_playlist/', views.create_playlist, name='create-playlist'),
    path('update_playlist/<int:pk>', views.update_playlist, name='update-playlist'),
    path('delete_playlist/<int:pk>', views.delete_playlist, name='delete-playlist'),

    #User accounts
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.registerPage, name='register_page'),

    # API
    path('spotify/top_artists/', views.get_top_artists, name='get-top-artists'),
    path('spotify/login/', views.spotify_login, name='spotify-login'),
    path('spotify/redirect/', views.spotify_redirect, name='spotify-redirect'),
]
