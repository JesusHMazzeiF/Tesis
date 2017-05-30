# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULAcode', '0005_framework_frameworktoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='framework',
            name='userToFramework',
            field=models.ManyToManyField(to='ULAcode.Usuario'),
        ),
        migrations.AddField(
            model_name='rolusuario',
            name='userToRol',
            field=models.ManyToManyField(to='ULAcode.Usuario'),
        ),
        migrations.AlterField(
            model_name='framework',
            name='urlFramework',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
