# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Chunk'
        db.create_table('chunks_chunk', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('content_pl', self.gf('markupfield.fields.MarkupField')(rendered_field=True, blank=True)),
            ('content_en', self.gf('markupfield.fields.MarkupField')(rendered_field=True, blank=True)),
            ('content_pl_markup_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
            ('content_en_markup_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
            ('_content_pl_rendered', self.gf('django.db.models.fields.TextField')()),
            ('_content_en_rendered', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('chunks', ['Chunk'])

        # Adding model 'Attachment'
        db.create_table('chunks_attachment', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('chunks', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Chunk'
        db.delete_table('chunks_chunk')

        # Deleting model 'Attachment'
        db.delete_table('chunks_attachment')


    models = {
        'chunks.attachment': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'chunks.chunk': {
            'Meta': {'ordering': "('key',)", 'object_name': 'Chunk'},
            '_content_en_rendered': ('django.db.models.fields.TextField', [], {}),
            '_content_pl_rendered': ('django.db.models.fields.TextField', [], {}),
            'content_en': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True', 'blank': 'True'}),
            'content_en_markup_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'content_pl': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True', 'blank': 'True'}),
            'content_pl_markup_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        }
    }

    complete_apps = ['chunks']