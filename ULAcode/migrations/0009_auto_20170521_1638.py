# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-21 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULAcode', '0008_auto_20170516_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolusuario',
            name='rol',
            field=models.CharField(choices=[('SysAdm', 'Administrador de Sistema'), ('FrameAdm', 'Administrador de Framework'), ('Usuario', 'Usuario Comun')], max_length=15, unique=True, verbose_name='Rol del Usuario'),
        ),
    ]
