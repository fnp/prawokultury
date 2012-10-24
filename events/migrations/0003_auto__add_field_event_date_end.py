# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.date_end'
        db.add_column('events_event', 'date_end',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, default='2000-01-01 0:00', max_length=255, blank=True),
                      keep_default=False)

        if not db.dry_run:
            orm.Event.objects.all().update(date_end=models.F('date'))

    def backwards(self, orm):
        # Deleting field 'Event.date_end'
        db.delete_column('events_event', 'date_end')


    models = {
        'events.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'max_length': '255', 'db_index': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
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