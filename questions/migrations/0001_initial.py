# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import taggit_autosuggest.managers
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='contact e-mail', blank=True)),
                ('question', models.TextField(verbose_name='question')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='changed at')),
                ('approved', models.BooleanField(default=False, verbose_name='approved')),
                ('edited_question', models.TextField(help_text="Leave empty if question doesn't need editing.", null=True, verbose_name='edited question', blank=True)),
                ('answer', markupfield.fields.MarkupField(help_text='Use <a href="http://txstyle.org/">Textile</a> syntax.', rendered_field=True, verbose_name='answer', blank=True)),
                ('answered_by', models.CharField(max_length=127, null=True, verbose_name='answered by', blank=True)),
                ('answer_markup_type', models.CharField(default=b'textile_pl', max_length=30, editable=False, choices=[(b'', b'--'), (b'textile_pl', b'textile_pl')])),
                ('answered', models.BooleanField(default=False, help_text='Check to send the answer to user.', db_index=True, verbose_name='answered')),
                ('_answer_rendered', models.TextField(editable=False)),
                ('answered_at', models.DateTimeField(db_index=True, null=True, verbose_name='answered at', blank=True)),
                ('published', models.BooleanField(default=False, help_text='Check to display answered question on site.', db_index=True, verbose_name='published')),
                ('published_at', models.DateTimeField(db_index=True, null=True, verbose_name='published at', blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('click_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag Category',
                'verbose_name_plural': 'Tag Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='questions_tagitem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='items', to='questions.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(related_name='tags', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='questions.TagCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=taggit_autosuggest.managers.TaggableManager(to='questions.Tag', through='questions.TagItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
