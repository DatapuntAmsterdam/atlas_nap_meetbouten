from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as geo

from datapunt_generic.generic import mixins

# from datasets.nap.models import Peilmerk


class Meetbout(mixins.ImportStatusMixin):
    STATUS_ACTUEEL = 'A'
    STATUS_VERVALLEN = 'V'

    STATUS_CHOICES = (
        (STATUS_ACTUEEL, 'actueel'),
        (STATUS_VERVALLEN, 'vervallen'),
    )

    id = models.CharField(max_length=10, primary_key=True)

    buurt = models.CharField(max_length=50, null=True)

    locatie_x = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    locatie_y = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    hoogte_nap = models.DecimalField(
            max_digits=settings.NAP_MAX_DIGITS,
            decimal_places=settings.NAP_DECIMAL_PLACES,
            null=True
    )
    zakking_cumulatief = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    datum = models.DateField(null=True)
    bouwblokzijde = models.CharField(max_length=10, null=True)
    eigenaar = models.CharField(max_length=50, null=True)
    beveiligd = models.BooleanField(default=False)
    deelraad = models.CharField(max_length=50, null=True)
    nabij_adres = models.CharField(max_length=255, null=True)
    locatie = models.CharField(max_length=50, null=True)
    zakkingssnelheid = models.DecimalField(
            max_digits=settings.ZAKKING_MAX_DIGITS,
            decimal_places=settings.ZAKKING_DECIMAL_PLACES,
            null=True
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)
    bouwbloknummer = models.CharField(max_length=4, null=True)
    blokeenheid = models.SmallIntegerField(null=True)

    rollaag = models.ForeignKey('Rollaag', related_name="meetbouten", null=True)

    geometrie = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __str__(self):
        return "{} ({})".format(self.nabij_adres, self.id)


class Referentiepunt(mixins.ImportStatusMixin):
    id = models.CharField(max_length=10, primary_key=True)
    locatie_x = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    locatie_y = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    hoogte_nap = models.DecimalField(
            max_digits=settings.NAP_MAX_DIGITS,
            decimal_places=settings.NAP_DECIMAL_PLACES,
            null=True
    )
    datum = models.DateField(null=True)
    locatie = models.CharField(max_length=255, null=True)
    geometrie = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __str__(self):
        return '{}'.format(self.pk)


class Meting(mixins.ImportStatusMixin):
    TYPE_NULMETING = 'N'
    TYPE_HERHALINGSMETING = 'H'
    TYPE_TUSSENTIJDS = 'T'
    TYPE_SCHATTING = 'S'

    TYPE_CHOICES = (
        (TYPE_NULMETING, 'nulmeting'),
        (TYPE_HERHALINGSMETING, 'herhalingsmeting'),
        (TYPE_TUSSENTIJDS, 'tussentijdse meting'),
        (TYPE_SCHATTING, 'schatting'),
    )

    id = models.CharField(max_length=10, primary_key=True)
    datum = models.DateField(null=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True)
    hoogte_nap = models.DecimalField(
        max_digits=settings.NAP_MAX_DIGITS,
        decimal_places=settings.NAP_DECIMAL_PLACES,
        null=True
    )
    zakking = models.DecimalField(
        max_digits=settings.ZAKKING_MAX_DIGITS,
        decimal_places=settings.ZAKKING_DECIMAL_PLACES,
        null=True
    )
    meetbout = models.ForeignKey(Meetbout, related_name="metingen")
    refereert_aan = models.ManyToManyField(
        Referentiepunt,
        through='ReferentiepuntMeting',
        related_name='metingen'
    )
    zakkingssnelheid = models.DecimalField(
        max_digits=settings.ZAKKING_MAX_DIGITS,
        decimal_places=settings.ZAKKING_DECIMAL_PLACES,
        null=True
    )
    zakking_cumulatief = models.DecimalField(
        max_digits=settings.ZAKKING_MAX_DIGITS,
        decimal_places=settings.ZAKKING_DECIMAL_PLACES,
        null=True
    )
    ploeg = models.CharField(max_length=50)
    type_int = models.SmallIntegerField(null=True)
    dagen_vorige_meting = models.IntegerField(default=0, null=True)
    pandmsl = models.CharField(max_length=50, null=True)
    deelraad = models.CharField(max_length=50, null=True)
    wvi = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '{}'.format(self.pk)


class ReferentiepuntMeting(models.Model):
    referentiepunt = models.ForeignKey(Referentiepunt)
    meting = models.ForeignKey(Meting)

    def __str__(self):
        return "{}-{}".format(self.referentiepunt_id, self.meting_id)


class Rollaag(mixins.ImportStatusMixin):
    id = models.IntegerField(primary_key=True)

    bouwblok = models.CharField(max_length=4, null=True)
    locatie_x = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    locatie_y = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            null=True
    )
    geometrie = geo.PointField(null=True, srid=28992)

    objects = geo.GeoManager()

    def __str__(self):
        return "{}".format(self.id)