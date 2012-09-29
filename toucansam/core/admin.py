from django.contrib import admin

from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from .models import Song


# show useful stuff...
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'key', 'singers')

    class Media:
        css = {
            "all": ("css/custom_admin.css",)
        }
admin.site.register(Song, SongAdmin)

# hide useless stuff...
admin.site.unregister(Group)
admin.site.unregister(Site)
