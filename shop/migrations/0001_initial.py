# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('migdal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='price', max_digits=6, decimal_places=2)),
                ('cost_const', models.DecimalField(max_digits=6, decimal_places=2)),
                ('cost_per_item', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('entry', models.OneToOneField(to='migdal.Entry', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['entry'],
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('items', models.IntegerField(default=1, verbose_name='items')),
                ('name', models.CharField(max_length=127, verbose_name='name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email', db_index=True)),
                ('address', models.TextField(verbose_name='address', db_index=True)),
                ('payed_at', models.DateTimeField(db_index=True, null=True, verbose_name='payed at', blank=True)),
                ('language_code', models.CharField(max_length=2, null=True, blank=True)),
                ('offer', models.ForeignKey(verbose_name='offer', on_delete=models.CASCADE, to='shop.Offer')),
            ],
            options={
                'ordering': ['-payed_at'],
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
            bases=(models.Model,),
        ),
    ]
