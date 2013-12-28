# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Song.difficulty'
        db.add_column(u'core_song', 'difficulty',
                      self.gf('django.db.models.fields.IntegerField')(default=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Song.difficulty'
        db.delete_column(u'core_song', 'difficulty')


    models = {
        u'core.gig': {
            'Meta': {'object_name': 'Gig'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.setitem': {
            'Meta': {'object_name': 'SetItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'set_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setitems'", 'to': u"orm['core.SetList']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setitems'", 'to': u"orm['core.Song']"})
        },
        u'core.setlist': {
            'Meta': {'object_name': 'SetList'},
            'gig': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Gig']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_proposed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'set_lists'", 'symmetrical': 'False', 'through': u"orm['core.SetItem']", 'to': u"orm['core.Song']"})
        },
        u'core.song': {
            'Meta': {'ordering': "['title']", 'object_name': 'Song'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cheat_sheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'lyrics_with_chords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'proposed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'run_time': ('durationfield.db.models.fields.duration.DurationField', [], {'default': '120000000'}),
            'singers': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'video_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['core']