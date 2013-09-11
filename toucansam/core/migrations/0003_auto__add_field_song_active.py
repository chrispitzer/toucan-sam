# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Song.active'
        db.add_column('core_song', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Song.active'
        db.delete_column('core_song', 'active')


    models = {
        'core.gig': {
            'Meta': {'object_name': 'Gig'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.setitem': {
            'Meta': {'object_name': 'SetItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'set_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setitems'", 'to': "orm['core.SetList']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setitems'", 'to': "orm['core.Song']"})
        },
        'core.setlist': {
            'Meta': {'object_name': 'SetList'},
            'gig': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Gig']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'set_lists'", 'symmetrical': 'False', 'through': "orm['core.SetItem']", 'to': "orm['core.Song']"})
        },
        'core.song': {
            'Meta': {'object_name': 'Song'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cheat_sheet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'lyrics_with_chords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'singers': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'video_link': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['core']