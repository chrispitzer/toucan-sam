# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gig'
        db.create_table('core_gig', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('core', ['Gig'])

        # Adding model 'SetItem'
        db.create_table('core_setitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Song'])),
            ('set_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SetList'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['SetItem'])

        # Adding model 'SetList'
        db.create_table('core_setlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gig', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Gig'])),
        ))
        db.send_create_signal('core', ['SetList'])


    def backwards(self, orm):
        # Deleting model 'Gig'
        db.delete_table('core_gig')

        # Deleting model 'SetItem'
        db.delete_table('core_setitem')

        # Deleting model 'SetList'
        db.delete_table('core_setlist')


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
            'set_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SetList']"}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Song']"})
        },
        'core.setlist': {
            'Meta': {'object_name': 'SetList'},
            'gig': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Gig']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'songs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'set_lists'", 'symmetrical': 'False', 'through': "orm['core.SetItem']", 'to': "orm['core.Song']"})
        },
        'core.song': {
            'Meta': {'object_name': 'Song'},
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