from django.contrib import admin

from django.contrib.auth.models import Group
from .models import Song, SetList, Gig


# show useful stuff...
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'key', 'singers', 'running_seconds', 'active')
    list_editable = ('singers', 'running_seconds', 'active')

    class Media:
        css = {
            "all": ("css/custom_admin.css",)
        }


admin.site.register(Song, SongAdmin)
admin.site.register(SetList)
admin.site.register(Gig)

# hide useless stuff...
admin.site.unregister(Group)