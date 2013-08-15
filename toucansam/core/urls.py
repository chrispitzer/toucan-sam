from django.conf.urls import patterns, url
from core.views import SetListView

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^songs/?$', 'core.views.song_list', name='song_list'),
    url(r'^setlist/(?P<set_list_id>\d+|new)/?$', SetListView.as_view(), name='set_list'),
    url(r'^songs/(?P<song_id>[0-9]+)?$', 'core.views.song',
        name='song'),
    url(r'^api/save_setlist/(?P<set_list_id>\d+|new)/?$', 'core.views.set_list_ajax'),
)
