# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Entry.changed_at'
        db.add_column('migdal_entry', 'changed_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2000, 1, 1, 0, 0), db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.published_at_pl'
        db.add_column('migdal_entry', 'published_at_pl',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Entry.published_at_en'
        db.add_column('migdal_entry', 'published_at_en',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        if not db.dry_run:
            for entry in orm['migdal.Entry'].objects.all():
                if entry.published_pl:
                    entry.published_at_pl = entry.date
                if entry.published_en:
                    entry.published_at_en = entry.date
                entry.save()


    def backwards(self, orm):
        # Deleting field 'Entry.changed_at'
        db.delete_column('migdal_entry', 'changed_at')

        # Deleting field 'Entry.published_at_pl'
        db.delete_column('migdal_entry', 'published_at_pl')

        # Deleting field 'Entry.published_at_en'
        db.delete_column('migdal_entry', 'published_at_en')


    models = {
        'migdal.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['migdal.Entry']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'migdal.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'slug_pl': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'taxonomy': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        'migdal.entry': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Entry'},
            '_body_en_rendered': ('django.db.models.fields.TextField', [], {}),
            '_body_pl_rendered': ('django.db.models.fields.TextField', [], {}),
            '_lead_en_rendered': ('django.db.models.fields.TextField', [], {}),
            '_lead_pl_rendered': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'body_en': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'body_pl': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'body_pl_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['migdal.Category']", 'null': 'True', 'blank': 'True'}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_en': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'lead_en_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'lead_pl': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'lead_pl_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'needed_en': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1', 'db_index': 'True'}),
            'promo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_at_en': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_at_pl': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_en': ('migdal.fields.SlugNullField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_pl': ('migdal.fields.SlugNullField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        }
    }

    complete_apps = ['migdal']