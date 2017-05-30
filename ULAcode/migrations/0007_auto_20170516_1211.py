# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ULAcode', '0006_auto_20170516_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='framework',
            name='frameworkToken',
            field=models.CharField(max_length=256, verbose_name='Token del API externa'),
        ),
        migrations.AlterField(
            model_name='framework',
            name='urlFramework',
            field=models.CharField(max_length=50, unique=True, verbose_name='URL del Framework'),
        ),
        migrations.AlterField(
            model_name='rolusuario',
            name='rol',
            field=models.CharField(max_length=15, unique=True, verbose_name='Rol del Usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cedula',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Cedula del Usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fotoAuth',
            field=models.ImageField(upload_to='authUsuario', verbose_name='Foto para Autenticacion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fotoPerfil',
            field=models.ImageField(upload_to='perfilUsuarios', verbose_name='Foto de Perfil'),
        ),
    ]