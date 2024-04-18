from django.contrib import admin
from .models import *

# Guardian
from guardian.admin import GuardedModelAdmin

class PlaylistUserAdmin(GuardedModelAdmin):
    pass

# Register your models here.
admin.site.register(Playlist, PlaylistUserAdmin)
admin.site.register(Artist)
admin.site.register(Genre)