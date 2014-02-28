from urlparse import urlparse, parse_qs
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from durationfield.db.models.fields.duration import DurationField


class ActiveSongsManager(models.Manager):
    def get_query_set(self):
        qs = super(ActiveSongsManager, self).get_query_set()
        qs = qs.filter(active=True)
        return qs


class Song(models.Model):
    title = models.CharField(max_length=255, blank=True)
    short_title = models.CharField(max_length=30, blank=True)
    artist = models.CharField(max_length=255, blank=True)

    key = models.CharField(max_length=25, blank=True)
    singers = models.CharField(max_length=255, blank=True)
    cheat_sheet = models.CharField(max_length=255, blank=True)
    lyrics_with_chords = models.TextField(blank=True)
    video_link = models.URLField(max_length=255, blank=True)
    run_time = DurationField(default=2*60*1000000)  # default: two minutes
    difficulty = models.IntegerField(default=3,
                                     choices=(
                                         (1, 'Real Easy'),
                                         (2, 'Easy'),
                                         (3, 'Normal'),
                                         (4, 'Hard'),
                                         (5, 'Real Hard'),
                                     ),
                                     validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])
    proposed = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveSongsManager()

    def save(self, *args, **kwargs):
        if not self.short_title and self.title:
            self.short_title = self.title[-30:]
        super(Song, self).save(*args, **kwargs)

    @property
    def milliseconds(self):
        return self.run_time.total_seconds() * 1000

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
    show_proposed = models.BooleanField(default=False)

    @property
    def name(self):
        return self.gig.name

    @property
    def ordered_songs(self):
        return self.songs.order_by('setitems__order')

    @property
    def run_time(self):
        microseconds = int(self.songs.aggregate(s=models.Sum('run_time'))['s'])
        return timedelta(microseconds=microseconds)

    def __unicode__(self):
        return self.name or "undefined"