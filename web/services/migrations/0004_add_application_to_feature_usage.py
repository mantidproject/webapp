# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-07 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_python2to3_conversion'),
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