# Generated by Django 2.1.2 on 2018-10-16 09:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peilmerk',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('hoogte', models.DecimalField(decimal_places=4, max_digits=10, null=True)),
                ('jaar', models.IntegerField(null=True)),
                ('merk', models.SmallIntegerField(choices=[(0, 'ronde bout met opschrift NAP (0)'), (1, 'ronde bout (aan de bovenzijde) zonder opschrift of met opschrift anders dan NAP (1)'), (2, 'kleine ronde bout (2)'), (3, 'knopbout (3)'), (4, 'vierkante bout met of zonder groeven (4)'), (5, 'kleine ronde kruisbout (5)'), (7, 'bijzondere merktekens, bijvoorbeeld zeskantige bout, stalen pen, enz. (7)'), (13, 'kopbout (13)'), (14, 'inbusbout (cilinderschroef met binnen zeskant) in slaganker M6 (14)'), (15, 'koperen hakkelbout (15)'), (16, 'koperen bout (16)'), (17, 'RVS-bout (17)'), (18, 'koperen bout met 3 Andreas kruizen (18)'), (99, 'onbekend (99)')], null=True)),
                ('omschrijving', models.TextField(null=True)),
                ('windrichting', models.CharField(max_length=2, null=True)),
                ('muurvlak_x', models.IntegerField(null=True)),
                ('muurvlak_y', models.IntegerField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
                ('rws_nummer', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]
