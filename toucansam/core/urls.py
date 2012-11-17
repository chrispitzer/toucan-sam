from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^songs/?$', 'core.views.song_list', name='song_list'),
    url(r'^songs/(?P<song_id>[0-9]+)?$', 'core.views.song',
        name='song'),
)
