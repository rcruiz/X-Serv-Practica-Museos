# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('contenido', models.TextField(default='')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('usuario', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Css',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('usuario', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('direccion', models.CharField(max_length=256)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('descripcion', models.TextField()),
                ('horario', models.CharField(max_length=256)),
                ('busMetro', models.CharField(max_length=256)),
                ('accesible', models.BooleanField(default=False)),
                ('barrio', models.CharField(max_length=64)),
                ('distrito', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=128, default='')),
                ('tlfno', models.CharField(max_length=12)),
                ('ncomment', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MuseoSeleccionado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('usuario', models.CharField(max_length=32)),
                ('museo', models.ForeignKey(to='museos.Museo')),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
