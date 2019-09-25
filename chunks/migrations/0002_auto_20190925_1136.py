# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chunk',
            options={'ordering': ('key',), 'verbose_name': 'chunk', 'verbose_name_plural': 'chunks'},
        ),
        migrations.AlterField(
            model_name='chunk',
            name='content_en_markup_type',
            field=models.CharField(default=b'textile_pl', max_length=30, editable=False, choices=[(b'', b'--'), (b'textile_pl', b'textile_pl')]),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='content_pl_markup_type',
            field=models.CharField(default=b'textile_pl', max_length=30, editable=False, choices=[(b'', b'--'), (b'textile_pl', b'textile_pl')]),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='key',
            field=models.CharField(help_text='A unique name for this chunk of content', max_length=255, serialize=False, verbose_name='key', primary_key=True),
        ),
    ]
