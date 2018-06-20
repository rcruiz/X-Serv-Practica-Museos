# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0005_auto_20180518_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='css',
            name='colorFondo',
            field=models.CharField(default='#efefef', max_length=32),
        ),
    ]
