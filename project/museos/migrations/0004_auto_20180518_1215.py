# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0003_auto_20180516_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='css',
            name='colorLetra',
        ),
        migrations.AddField(
            model_name='css',
            name='colorFondo',
            field=models.CharField(max_length=32, default='#eaeaea'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='museoseleccionado',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
