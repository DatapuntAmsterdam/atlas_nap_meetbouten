import csv
import datetime
import logging
import os

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from batch import batch
from batch import csv as dp_csv
from batch.clear import clear_models
from batch import metadata


from .models import Peilmerk

log = logging.getLogger(__name__)


class ImportNapTask(batch.BasicTask):
    name = "Import NAP"
    dataset_id = "NAP"
    peilmerken = dict()
    merk_choices = dict()

    def __init__(self, path):
        self.path = path

    def before(self):
        self.merk_choices = dict(Peilmerk.MERK_CHOICES)
        clear_models(Peilmerk)

    def after(self):
        metadata.upload(self.dataset_id, self.mdate.year,
                        self.mdate.month, self.mdate.day)

    def process(self):
        source = os.path.join(self.path, "NAP_PEILMERK.dat")
        self.mdate = datetime.date.fromtimestamp(os.path.getmtime(source))
        with open(source, encoding='cp1252') as f:
            rows = csv.reader(
                f, delimiter='|', quotechar='$', doublequote=True)
            self.peilmerken = [result for result in
                               (self.process_row(row) for row in rows) if
                               result]

        Peilmerk.objects.bulk_create(
            self.peilmerken,
            batch_size=settings.BATCH_SIZE)

    def process_row(self, r):
        row = dp_csv.cleanup_row(r, replace=True)

        pk = row[0]
        merk = int(row[3])

        if merk not in self.merk_choices:
            log.warning(
                "Peilmerk {} references non-existing merk {}; skipping".format(
                    pk, merk))
            return

        # PEILMERKNR,HOOGTE,JAAR,MERK,OMSCHRIJVING,WINDRICHTING,X_MUURVLAK,Y_MUURVLAK,RWSNR,GEOMETRIE
        return Peilmerk(
            pk=pk,
            hoogte=dp_csv.parse_decimal(row[1]),
            jaar=int(row[2]),
            merk=int(row[3]),
            omschrijving=row[4],
            windrichting=row[5],
            muurvlak_x=int(row[6] or 0),
            muurvlak_y=int(row[7] or 0),
            rws_nummer=row[8],
            geometrie=GEOSGeometry(row[9]),
        )


class ImportNapJob(object):
    name = "Import NAP"

    def __init__(self):
        diva = settings.DIVA_DIR
        if not os.path.exists(diva):
            raise ValueError("DIVA_DIR not found: {}".format(diva))

        self.nap = os.path.join(diva, 'nap')

    def tasks(self):
        return [
            ImportNapTask(self.nap)
        ]
