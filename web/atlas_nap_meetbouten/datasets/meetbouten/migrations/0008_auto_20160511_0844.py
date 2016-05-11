# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-11 08:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetbouten', '0007_auto_20160321_1032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetbout',
            old_name='nabij_adres',
            new_name='adres',
        ),
        migrations.RenameField(
            model_name='meetbout',
            old_name='locatie_x',
            new_name='x_coordinaat',
        ),
        migrations.RenameField(
            model_name='meetbout',
            old_name='locatie_y',
            new_name='y_coordinaat',
        ),
        migrations.RenameField(
            model_name='referentiepunt',
            old_name='locatie_x',
            new_name='x_coordinaat',
        ),
        migrations.RenameField(
            model_name='referentiepunt',
            old_name='locatie_y',
            new_name='y_coordinaat',
        ),
        migrations.RenameField(
            model_name='rollaag',
            old_name='locatie_x',
            new_name='x_coordinaat',
        ),
        migrations.RenameField(
            model_name='rollaag',
            old_name='locatie_y',
            new_name='y_coordinaat',
        ),
    ]