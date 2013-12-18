from django.conf.urls import patterns, url
from core.views import SetListView, CheatSheetView, SetListAjax, RandoColor, SetListSecondsjaxView

urlpatterns = patterns('',
    url(r'^/?$', 'core.views.song_list', name='song_list'),
    url(r'^songs/?$', 'core.views.song_list', name='song_list'),
    url(r'^set_list/(?P<set_list_id>\d+|new)/?$', SetListView.as_view(), name='set_list'),
    url(r'^songs/(?P<song_id>[0-9]+)?$', 'core.views.song',
        name='song'),
    url(r'^set_list_list/', 'core.views.set_list_list', name='set_list_list'),
    url(r'^cheat_sheet/(?P<set_list_id>\d+)/?$', CheatSheetView.as_view(), name="cheat_sheet"),
    url(r'^master_cheat_sheet/', CheatSheetView.as_view(), name="master_cheat_sheet"),
    url(r'^api/save_set_list/(?P<set_list_id>\d+|new)/?$', SetListAjax.as_view(), name="set_list_ajax"),
    url(r'^api/randocolor/?$', RandoColor.as_view(), name="rando_color"),
    url(r'^api/setlist_runtime/(?P<set_list_id>\d+|new)/?$', SetListSecondsjaxView.as_view(), name="set_list_time"),
)
