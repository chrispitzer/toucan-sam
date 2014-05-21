import re
from urlparse import urlparse, parse_qs
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
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

    @property
    def column_width(self):
        return reduce(lambda a, b: max(a, len(b)), re.split("[\r\n]+", self.lyrics_with_chords), 0)

    @property
    def lyrics_formatted(self):
        """
        Assumes that lyrics with chords interleaves lines with chords and lines with lyrics
        """
        def tokenize(s):
            return re.split(r'(\w+)', s)
        def chordify(chord, cssclass="chord"):
            return '<span class="{}">{}</span>'.format(cssclass, chord)
        def lineify(line):
            return "<p>{}</p>".format(line)

        output = []
        chord_line = None
        chord_regex = re.compile(r"^(\W*[ABCDEFG]b?(m|min|maj|maj)?\d*\W*)+$", flags=re.IGNORECASE)
        for line in re.split("[\r\n]+", self.lyrics_with_chords):
            line = line.rstrip()
            if chord_regex.match(line):
                if chord_line:
                    formatted_line = ""
                    for chord in tokenize(chord_line):
                        if re.match("\W", chord):
                            formatted_line += chord
                        else:
                            formatted_line += chordify(chord, cssclass="chord inline")
                    output.append(lineify(formatted_line))

                chord_line = line
                continue
            if chord_line:
                formatted_line = ""
                line = line.ljust(len(chord_line))
                chords = tokenize(chord_line)
                for chord in chords:
                    l = len(chord)
                    if not (chord+" ").isspace():
                        formatted_line += chordify(chord)
                    formatted_line += line[:l]
                    line = line[l:]
                line = formatted_line + line
                chord_line = None

            output.append(lineify(line))

        return mark_safe("\n".join(output))  # todo: sanitize input

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