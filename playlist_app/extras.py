from .models import Token
from .credentials import *
from django.utils import timezone
from datetime import timedelta
from requests import post

BASE_URL = "https://api.spotify.com/v1/search"

# Check Tokens
def check_tokens(session_id):
    tokens = Token.objects.filter(user = session_id)
    if tokens:
        return tokens[0]
    else:
        return None
    
# Create and Update token model
def create_or_update_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    # Update tokens if they exist
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = Token(
            user = session_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
            token_type = token_type
        )
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)

    if tokens:
        if tokens.expires_in <= timezone.now():
            pass
        return True
    return False

def refresh_token_func(session_id):
    refresh_token = check_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token':refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')

    create_or_update_tokens(
        session_id = session_id,
        access_token = access_token,
        refresh_token = refresh_token,
        expires_in = expires_in,
        token_type = token_type
    )
