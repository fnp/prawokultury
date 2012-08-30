# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.published_pl'
        db.add_column('events_event', 'published_pl',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Event.published_en'
        db.add_column('events_event', 'published_en',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        if not db.dry_run:
            orm.Event.objects.all().update(published_pl=True, published_en=True)


    def backwards(self, orm):
        # Deleting field 'Event.published_pl'
        db.delete_column('events_event', 'published_pl')

        # Deleting field 'Event.published_en'
        db.delete_column('events_event', 'published_en')


    models = {
        'events.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'organizer_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'organizer_pl': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'place_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'place_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'published_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['events']