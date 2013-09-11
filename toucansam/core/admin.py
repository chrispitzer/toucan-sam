from django.contrib import admin

from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from .models import Song, SetList, Gig


# show useful stuff...
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'key', 'singers', 'active')
    list_editable = ('singers', 'active')

    def queryset(self, request):
        return Song.all_objects.all()

    class Media:
        css = {
            "all": ("css/custom_admin.css",)
        }


admin.site.register(Song, SongAdmin)
admin.site.register(SetList)
admin.site.register(Gig)

# hide useless stuff...
admin.site.unregister(Group)
admin.site.unregister(Site)