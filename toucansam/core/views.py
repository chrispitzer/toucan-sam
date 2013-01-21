from lib.decorators import template

from django.shortcuts import get_object_or_404

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


@template("set_list.html")
def set_list(request):
    songs = models.Song.objects.all()
    return {
        "songs":songs,
    }


@template("song.html")
def song(request, song_id):
    song = get_object_or_404(models.Song, id=song_id)
    return {
        "song":song,
    }
