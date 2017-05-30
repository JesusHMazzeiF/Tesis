# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULAcode', '0020_auto_20170522_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='framework',
            name='id',
        ),
        migrations.AlterField(
            model_name='framework',
            name='urlFramework',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='URL del Framework'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='userRol',
            field=models.ManyToManyField(to='ULAcode.RolUsuario'),
        ),
    ]
