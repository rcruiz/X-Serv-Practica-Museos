# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='css',
            name='Titulo',
            field=models.CharField(max_length=32, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='css',
            name='colorLetra',
            field=models.CharField(max_length=32, default=''),
        ),
        migrations.AddField(
            model_name='css',
            name='tamLetra',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]
