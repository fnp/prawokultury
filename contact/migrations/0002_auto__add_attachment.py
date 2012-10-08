# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attachment'
        db.create_table('contact_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contact.Contact'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('contact', ['Attachment'])

        # Adding index on 'Contact', fields ['form_tag']
        db.create_index('contact_contact', ['form_tag'])


    def backwards(self, orm):
        # Removing index on 'Contact', fields ['form_tag']
        db.delete_index('contact_contact', ['form_tag'])

        # Deleting model 'Attachment'
        db.delete_table('contact_attachment')


    models = {
        'contact.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Contact']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'contact.contact': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contact'},
            'body': ('jsonfield.fields.JSONField', [], {}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form_tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['contact']