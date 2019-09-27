# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('key', models.CharField(help_text='A unique name for this attachment', max_length=255, serialize=False, verbose_name='key', primary_key=True)),
                ('attachment', models.FileField(upload_to=b'chunks/attachment')),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('key', models.CharField(help_text='A unique name for this piece of content', max_length=255, serialize=False, verbose_name='key', primary_key=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('content_pl', markupfield.fields.MarkupField(help_text='Use <a href="http://txstyle.org/">Textile</a> syntax.', rendered_field=True, verbose_name='content', blank=True)),
                ('content_en', markupfield.fields.MarkupField(help_text='Use <a href="http://txstyle.org/">Textile</a> syntax.', rendered_field=True, verbose_name='content', blank=True)),
                ('content_pl_markup_type', models.CharField(default=b'textile_pl', max_length=30, editable=False, choices=[(b'', b'--'), (b'textile_pl', b'textile_pl')])),
                ('content_en_markup_type', models.CharField(default=b'textile_pl', max_length=30, editable=False, choices=[(b'', b'--'), (b'textile_pl', b'textile_pl')])),
                ('_content_pl_rendered', models.TextField(editable=False)),
                ('_content_en_rendered', models.TextField(editable=False)),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'piece',
                'verbose_name_plural': 'pieces',
            },
            bases=(models.Model,),
        ),
    ]
