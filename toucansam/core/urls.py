from django.conf.urls import patterns, url
from core import views

urlpatterns = patterns('',
    url(r'^/?$', views.SongListView.as_view(), name='song_list'),
    url(r'^songs/?$', views.SongListView.as_view(), name='song_list'),
    url(r'^set_list/(?P<set_list_id>\d+|new)/?$', views.SetListView.as_view(), name='set_list'),
    url(r'^songs/(?P<song_id>[0-9]+)/??$', views.SongView.as_view(), name='song'),
    url(r'^songs/(?P<song_id>[0-9]+)/print/?$', views.PrintSongView.as_view(), name='print_song'),
    url(r'^set_list_list/', 'core.views.set_list_list', name='set_list_list'),
    url(r'^cheat_sheet/(?P<set_list_id>\d+)/?$', views.CheatSheetView.as_view(), name="cheat_sheet"),
    url(r'^master_cheat_sheet/', views.CheatSheetView.as_view(), name="master_cheat_sheet"),
    url(r'^api/save_set_list/(?P<set_list_id>\d+|new)/?$', views.SetListAjax.as_view(), name="set_list_ajax"),
    url(r'^api/randocolor/?$', views.RandoColor.as_view(), name="rando_color"),
    url(r'^api/setlist_runtime/(?P<set_list_id>\d+|new)/?$', views.SetListSecondsjaxView.as_view(), name="set_list_time"),
    url(r'^api/add_to_setlist/(?P<set_list_id>\d+|new)/?$', views.UpdateSetListAjax.as_view(), name="add_to_setlist"),
)
