# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Entry.slug_pl'
        db.alter_column('migdal_entry', 'slug_pl', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True))

        # Changing field 'Entry.title_pl'
        db.alter_column('migdal_entry', 'title_pl', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Entry.lead_pl'
        db.alter_column('migdal_entry', 'lead_pl', self.gf('markupfield.fields.MarkupField')(null=True, rendered_field=True))

    def backwards(self, orm):

        # Changing field 'Entry.slug_pl'
        db.alter_column('migdal_entry', 'slug_pl', self.gf('django.db.models.fields.SlugField')(default='', max_length=50, unique=True))

        # Changing field 'Entry.title_pl'
        db.alter_column('migdal_entry', 'title_pl', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Entry.lead_pl'
        db.alter_column('migdal_entry', 'lead_pl', self.gf('markupfield.fields.MarkupField')(default='', rendered_field=True))

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
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lead_en': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'lead_en_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'lead_pl': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'lead_pl_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'needed_en': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1', 'db_index': 'True'}),
            'promo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_pl': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        }
    }

    complete_apps = ['migdal']