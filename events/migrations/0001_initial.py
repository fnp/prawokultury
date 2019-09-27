# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(max_length=255, verbose_name='date', db_index=True)),
                ('date_end', models.DateTimeField(db_index=True, max_length=255, verbose_name='end date', blank=True)),
                ('link', models.URLField(verbose_name='link')),
                ('title_pl', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('organizer_pl', models.CharField(db_index=True, max_length=255, verbose_name='organizer', blank=True)),
                ('organizer_en', models.CharField(db_index=True, max_length=255, verbose_name='organizer', blank=True)),
                ('place_pl', models.CharField(max_length=255, verbose_name='place', blank=True)),
                ('place_en', models.CharField(max_length=255, verbose_name='place', blank=True)),
                ('published_pl', models.BooleanField(default=False, verbose_name='published')),
                ('published_en', models.BooleanField(default=False, verbose_name='published')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
            bases=(models.Model,),
        ),
    ]
