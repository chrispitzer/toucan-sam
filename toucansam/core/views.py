from lib.decorators import template

from . import models


@template("home.html")
def home(request):
    print "HOME"


@template("song_list.html")
def song_list(request):
    songs = models.Song.objects.all()
    return {
        "songs":songs,
    }


@template("song.html")
def song(request, song_id):
    print "particular: %s" % song_id
