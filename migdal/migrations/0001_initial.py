# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('migdal_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug_pl', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('slug_en', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64, db_index=True)),
        ))
        db.send_create_signal('migdal', ['Category'])

        # Adding model 'Entry'
        db.create_table('migdal_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=128, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('promo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug_pl', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lead_pl', self.gf('markupfield.fields.MarkupField')(rendered_field=True)),
            ('lead_pl_markup_type', self.gf('django.db.models.fields.CharField')(default='textile_pl', max_length=30)),
            ('_lead_pl_rendered', self.gf('django.db.models.fields.TextField')()),
            ('slug_en', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('lead_en', self.gf('markupfield.fields.MarkupField')(null=True, rendered_field=True, blank=True)),
            ('needed_en', self.gf('django.db.models.fields.CharField')(default='n', max_length=1, db_index=True)),
            ('lead_en_markup_type', self.gf('django.db.models.fields.CharField')(default='textile_pl', max_length=30, blank=True)),
            ('_lead_en_rendered', self.gf('django.db.models.fields.TextField')()),
            ('body_pl', self.gf('markupfield.fields.MarkupField')(null=True, rendered_field=True, blank=True)),
            ('body_en', self.gf('markupfield.fields.MarkupField')(null=True, rendered_field=True, blank=True)),
            ('body_pl_markup_type', self.gf('django.db.models.fields.CharField')(default='textile_pl', max_length=30, blank=True)),
            ('body_en_markup_type', self.gf('django.db.models.fields.CharField')(default='textile_pl', max_length=30, blank=True)),
            ('published_pl', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_en', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_body_pl_rendered', self.gf('django.db.models.fields.TextField')()),
            ('_body_en_rendered', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('migdal', ['Entry'])

        # Adding M2M table for field categories on 'Entry'
        db.create_table('migdal_entry_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['migdal.entry'], null=False)),
            ('category', models.ForeignKey(orm['migdal.category'], null=False))
        ))
        db.create_unique('migdal_entry_categories', ['entry_id', 'category_id'])

        # Adding model 'Attachment'
        db.create_table('migdal_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['migdal.Entry'])),
        ))
        db.send_create_signal('migdal', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('migdal_category')

        # Deleting model 'Entry'
        db.delete_table('migdal_entry')

        # Removing M2M table for field categories on 'Entry'
        db.delete_table('migdal_entry_categories')

        # Deleting model 'Attachment'
        db.delete_table('migdal_attachment')


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
            'lead_pl': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True'}),
            'lead_pl_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30'}),
            'needed_en': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1', 'db_index': 'True'}),
            'promo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_pl': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'})
        }
    }

    complete_apps = ['migdal']