# Generated by Django 2.1.2 on 2018-10-16 09:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meetbout',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('buurt', models.CharField(max_length=50, null=True)),
                ('x_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('y_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('hoogte_nap', models.DecimalField(decimal_places=4, max_digits=7, null=True)),
                ('zakking_cumulatief', models.DecimalField(decimal_places=13, max_digits=20, null=True)),
                ('datum', models.DateField(null=True)),
                ('bouwblokzijde', models.CharField(max_length=10, null=True)),
                ('eigenaar', models.CharField(max_length=50, null=True)),
                ('beveiligd', models.NullBooleanField(default=None)),
                ('stadsdeel', models.CharField(max_length=50, null=True)),
                ('adres', models.CharField(max_length=255, null=True)),
                ('locatie', models.CharField(max_length=50, null=True)),
                ('zakkingssnelheid', models.DecimalField(decimal_places=13, max_digits=20, null=True)),
                ('status', models.CharField(choices=[('A', 'actueel'), ('V', 'vervallen')], max_length=1, null=True)),
                ('bouwbloknummer', models.CharField(max_length=4, null=True)),
                ('blokeenheid', models.SmallIntegerField(null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
            ],
        ),
        migrations.CreateModel(
            name='Meting',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('datum', models.DateField(null=True)),
                ('type', models.CharField(choices=[('N', 'nulmeting'), ('H', 'herhalingsmeting'), ('T', 'tussentijdse meting'), ('S', 'schatting')], max_length=1, null=True)),
                ('hoogte_nap', models.DecimalField(decimal_places=4, max_digits=7, null=True)),
                ('zakking', models.DecimalField(decimal_places=13, max_digits=20, null=True)),
                ('zakkingssnelheid', models.DecimalField(decimal_places=13, max_digits=20, null=True)),
                ('zakking_cumulatief', models.DecimalField(decimal_places=13, max_digits=20, null=True)),
                ('ploeg', models.CharField(max_length=50)),
                ('type_int', models.SmallIntegerField(null=True)),
                ('dagen_vorige_meting', models.IntegerField(default=0, null=True)),
                ('pandmsl', models.CharField(max_length=50, null=True)),
                ('stadsdeel', models.CharField(max_length=50, null=True)),
                ('wvi', models.CharField(max_length=50, null=True)),
                ('meetbout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metingen', to='meetbouten.Meetbout')),
            ],
        ),
        migrations.CreateModel(
            name='Referentiepunt',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('x_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('y_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('hoogte_nap', models.DecimalField(decimal_places=4, max_digits=7, null=True)),
                ('datum', models.DateField(null=True)),
                ('locatie', models.CharField(max_length=255, null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
            ],
        ),
        migrations.CreateModel(
            name='ReferentiepuntMeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetbouten.Meting')),
                ('referentiepunt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meetbouten.Referentiepunt')),
            ],
        ),
        migrations.CreateModel(
            name='Rollaag',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('bouwblok', models.CharField(max_length=4, null=True)),
                ('x_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('y_coordinaat', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
            ],
        ),
        migrations.AddField(
            model_name='meting',
            name='refereert_aan',
            field=models.ManyToManyField(related_name='metingen', through='meetbouten.ReferentiepuntMeting', to='meetbouten.Referentiepunt'),
        ),
        migrations.AddField(
            model_name='meetbout',
            name='rollaag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meetbouten', to='meetbouten.Rollaag'),
        ),
    ]