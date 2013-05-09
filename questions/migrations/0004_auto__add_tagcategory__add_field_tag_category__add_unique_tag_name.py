# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagCategory'
        db.create_table('questions_tagcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('questions', ['TagCategory'])

        # Adding field 'Tag.category'
        db.add_column('questions_tag', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.TagCategory'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('questions_tag', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('questions_tag', ['name'])

        # Deleting model 'TagCategory'
        db.delete_table('questions_tagcategory')

        # Deleting field 'Tag.category'
        db.delete_column('questions_tag', 'category_id')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questions.question': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Question'},
            '_answer_rendered': ('django.db.models.fields.TextField', [], {}),
            'answer': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True', 'blank': 'True'}),
            'answer_markup_type': ('django.db.models.fields.CharField', [], {'default': "'textile_pl'", 'max_length': '30', 'blank': 'True'}),
            'answered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'answered_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited_question': ('django.db.models.fields.TextField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'db_index': 'True'})
        },
        'questions.tag': {
            'Meta': {'object_name': 'Tag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.TagCategory']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'questions.tagcategory': {
            'Meta': {'object_name': 'TagCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'questions.tagitem': {
            'Meta': {'object_name': 'TagItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions_tagitem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['questions.Tag']"})
        }
    }

    complete_apps = ['questions']