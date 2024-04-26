from django.shortcuts import redirect
from django.contrib import messages
from .models import *

# creating decorators
def user_is_owner():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # kwargs holds playlist pk
            print('KWARGS:', kwargs)
            # Getting the user from request
            user = request.user
            print('USER:',user,'\n')
            print('USER STAFF:',user.is_staff,'\n')
            pk = kwargs['pk']
            # Getting playlist associated with user
            playlist = Playlist.objects.get(id=pk)
            print(playlist.user)

            # Seeing if the user is the user associated with playlist
            if user == playlist.user or user.is_staff == True:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to perform that action')
                return redirect('playlist-detail', pk)
        return wrapper_func
    return decorator