from urlparse import urlparse, parse_qs
from django.core.urlresolvers import reverse
from django.db import models


class ActiveSongsManager(models.Manager):
    def get_query_set(self):
        qs = super(ActiveSongsManager, self).get_query_set()
        qs = qs.filter(active=True)
        return qs


class Song(models.Model):
    title = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)

    key = models.CharField(max_length=25, blank=True)
    singers = models.CharField(max_length=255, blank=True)
    cheat_sheet = models.CharField(max_length=255, blank=True)
    lyrics_with_chords = models.TextField(blank=True)
    video_link = models.URLField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    objects = ActiveSongsManager()
    all_objects = models.Manager()

    def has_no_lyrics(self):
        return len(self.lyrics_with_chords) < 50

    def youtube_video_id(self):
        try:
            parsed = urlparse(self.video_link)
            if parsed.netloc.endswith('youtube.com'):
                query = parse_qs(parsed.query)
                return query.get('v', [None])[0]
        except:
            return None

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('song', args=[self.id])

    class Meta:
        ordering = ["title"]


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