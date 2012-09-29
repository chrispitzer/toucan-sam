from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)

    key = models.CharField(max_length=25, blank=True)
    singers = models.CharField(max_length=255, blank=True)
    cheat_sheet = models.CharField(max_length=255, blank=True)
    lyrics_with_chords = models.TextField(blank=True)
    video_link = models.URLField(max_length=255, blank=True)
