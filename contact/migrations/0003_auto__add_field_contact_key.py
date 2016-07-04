# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contact.key'
        db.add_column(u'contact_contact', 'key',
                      self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=64, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contact.key'
        db.delete_column(u'contact_contact', 'key')


    models = {
        u'contact.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contact.Contact']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'contact.contact': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Contact'},
            'body': ('jsonfield.fields.JSONField', [], {}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form_tag': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'key': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']