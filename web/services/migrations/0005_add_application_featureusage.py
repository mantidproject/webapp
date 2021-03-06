# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-14 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_expand_field_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureusage',
            name='application',
            field=models.CharField(default='mantidplot', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='featureusage',
            unique_together=set([('mantidVersion', 'type', 'name', 'internal', 'application')]),
        ),
    ]
