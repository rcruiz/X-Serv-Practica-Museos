# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0004_auto_20180518_1215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='css',
            old_name='Titulo',
            new_name='titulo',
        ),
    ]
