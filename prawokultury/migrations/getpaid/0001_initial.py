# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payment'
        db.create_table(u'getpaid_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=20, db_index=True)),
            ('backend', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('paid_on', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, db_index=True, blank=True)),
            ('amount_paid', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=20, decimal_places=4)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment', to=orm['shop.Order'])),
        ))
        db.send_create_signal(u'getpaid', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Payment'
        db.delete_table(u'getpaid_payment')


    models = {
        u'getpaid.payment': {
            'Meta': {'ordering': "('-created_on',)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'amount_paid': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'backend': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment'", 'to': u"orm['shop.Order']"}),
            'paid_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20', 'db_index': 'True'})
        },
        u'migdal.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug_en': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'slug_pl': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'taxonomy': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'}),
            'title_pl': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'db_index': 'True'})
        },
        u'migdal.entry': {
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
            'canonical_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['migdal.Category']", 'null': 'True', 'blank': 'True'}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'first_published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_stream': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        },
        u'shop.offer': {
            'Meta': {'ordering': "['entry']", 'object_name': 'Offer'},
            'cost_const': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cost_per_item': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'entry': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['migdal.Entry']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'shop.order': {
            'Meta': {'ordering': "['-payed_at']", 'object_name': 'Order'},
            'address': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Offer']"}),
            'payed_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['getpaid']