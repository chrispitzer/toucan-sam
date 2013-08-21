from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)

    key = models.CharField(max_length=25, blank=True)
    singers = models.CharField(max_length=255, blank=True)
    cheat_sheet = models.CharField(max_length=255, blank=True)
    lyrics_with_chords = models.TextField(blank=True)
    video_link = models.URLField(max_length=255, blank=True)

    def has_no_lyrics(self):
        return len(self.lyrics_with_chords) < 50


class Gig(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name or "undefined"


class SetItem(models.Model):
    song = models.ForeignKey(Song, related_name='setitems')
    set_list = models.ForeignKey("SetList", related_name='setitems')
    order = models.IntegerField()


class SetList(models.Model):
    gig = models.ForeignKey(Gig)
    songs = models.ManyToManyField(Song, related_name="set_lists", through=SetItem)

    @property
    def name(self):
        return self.gig.name

    @property
    def ordered_songs(self):
        return self.songs.order_by('setitems__order')

    def __unicode__(self):
        return self.name or "undefined"