# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(max_length=255, db_index=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organizer_pl', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('organizer_en', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('place_pl', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('place_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('events', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('events_event')


    models = {
        'events.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'organizer_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'organizer_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'place_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']