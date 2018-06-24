# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0006_auto_20180619_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='css',
            name='tamLetra',
            field=models.CharField(max_length=4, default='12px'),
        ),
    ]
