# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-10-01 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, verbose_name='email'),
        ),
    ]