"""
Module Contains logic to get the latest most up to date
files to import in the NAP database

Goal is to assure we load Datapunt with accurate and current data

checks:

   check AGE of filenames
     - we do not work with old data
   check filename changes
     - we do not work of old files because new files are renamed

We download specific zip files:

Unzip target data in to empty new location and start
import proces.


"""
import argparse
import logging
import os
import time

import datetime
import zipfile

from functools import lru_cache
from dateutil import parser
from pathlib import Path


from swiftclient.client import Connection

log = logging.getLogger(__name__)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

connections = {
    'bag_brk': {
        'auth_version': '2.0',
        'authurl': 'https://identity.stack.cloudvps.com/v2.0',
        'user': 'bag_brk',
        'key': os.getenv('BAG_OBJECTSTORE_PASSWORD', 'insecure'),
        'tenant_name': 'BGE000081_BAG',
        'os_options': {
            'tenant_id': '4f2f4b6342444c84b3580584587cfd18',
            'region_name': 'NL',
        }
    },
    'GOB_user': {
        'auth_version': '2.0',
        'authurl': 'https://identity.stack.cloudvps.com/v2.0',
        'user': 'GOB_user',
        'key': os.getenv('GOB_OBJECTSTORE_PASSWORD', 'insecure'),
        'tenant_name': 'BGE000081_GOB',
        'os_options': {
            'tenant_id': '2ede4a78773e453db73f52500ef748e5',
            'region_name': 'NL',
        }
    }
}

DIVA_DIR = '/app/data'


@lru_cache(maxsize=None)
def get_conn(connect):
    assert (connect == 'bag_brk' and os.getenv('BAG_OBJECTSTORE_PASSWORD')) or (
                connect == 'GOB_user' and os.getenv('GOB_OBJECTSTORE_PASSWORD'))
    return Connection(**connections[connect])


def file_exists(target):
    target = Path(target)
    return target.is_file()


def get_full_container_list(connect, container_name, **kwargs):
    limit = 10000
    kwargs['limit'] = limit
    page = []
    seed = []
    _, page = get_conn(connect).get_container(container_name, **kwargs)
    seed.extend(page)

    while len(page) == limit:
        # keep getting pages..
        kwargs['marker'] = seed[-1]['name']
        _, page = get_conn(connect).get_container(container_name, **kwargs)
        seed.extend(page)

    return seed


def download_file(connect, container_name, file_path, target_path=None, file_last_modified=None):
    path = file_path.split('/')

    file_name = path[-1]
    log.info(f"Create file {file_name} in {DIVA_DIR}")
    file_name = path[-1]

    if target_path:
        newfilename = '{}/{}'.format(DIVA_DIR, target_path)
    else:
        newfilename = '{}/{}'.format(DIVA_DIR, file_name)

    if file_exists(newfilename):
        log.debug('Skipped file exists: %s', newfilename)
        return

    with open(newfilename, 'wb') as newfile:
        data = get_conn(connect).get_object(container_name, file_path)[1]
        newfile.write(data)
    if file_last_modified:
        epoch_modified = file_last_modified.timestamp()
        os.utime(newfilename, (epoch_modified, epoch_modified))


def download_diva_file(container_name, file_path, target_path=None):
    """
    Download a diva file
    """
    download_file('bag_brk', container_name, file_path, target_path=None)


def download_zips(container_name, zips_mapper):
    """
    Download latest zips
    """

    for _, zipfiles in zips_mapper.items():
        zipfiles.sort(reverse=True)
        zip_name = zipfiles[0][1]['name']
        download_diva_file(container_name, zip_name)


zip_age_limits = {
  'NAP.zip': 30,
  'MBT.zip': 30,
}


def check_age(zip_created, file_key, file_object):
    """
    Do basic sanity check on zip delivery..
    """

    now = datetime.datetime.today()
    delta = now - zip_created
    log.debug('AGE: %2d days', delta.days)
    source_name = file_object['name']

    log.debug('%s_%s' % (zip_created.strftime('%Y%m%d'), file_key))

    for key, agelimit in zip_age_limits.items():
        if file_key.endswith(key):
            if zip_age_limits[key] < delta.days:
                raise ValueError(
                    f"""

        Zip delivery is late!

        {key} age: {delta.days}  max_age: {zip_age_limits[key]}

        from {source_name}

                    """)


def validate_age(zips_mapper):
    """
    Check if the files we want to import are not to old!
    """
    log.debug('validating age..')

    for zipkey, zipfiles in zips_mapper.items():

        # this is the file we want to import
        age, importsource = zipfiles[0]

        check_age(age, zipkey, importsource)

        log.debug('OK: %s %s', age, zipkey)


def create_target_directories():
    """
    the directories where the import proces expects the import source files
    should be created before unzipping files.
    """

    # Make sure target directories exist
    for target in path_mapping.values():
        directory = os.path.join(DIVA_DIR, target)
        if not os.path.exists(directory):
            os.makedirs(directory)


path_mapping = {
    'MBT': 'meetbouten',
    'NAP': 'nap',
}


def unzip_files(zipsource, mtime):
    """
    Unzip single files to the right target directory
    """

    # Extract files to the expected location
    directory = os.path.join(DIVA_DIR)

    for fullname in zipsource.namelist():
        zipsource.extract(fullname, directory)
        file_name = fullname.split('/')[-1]
        for path, target in path_mapping.items():
            if path in fullname:
                source = f"{directory}/{fullname}"
                target = f'{directory}/{target}/{file_name}'
                # relocate fiel to expected location
                print(source)
                print(target)
                os.rename(source, target)
                # set modification date from zipfile
                os.utime(target, (mtime, mtime))


gob_file_age_and_target_list = {
    'meetbouten/DAT/MBT_MEETBOUT.dat': (30, 'meetbouten/MBT_MEETBOUT.dat'),
    'meetbouten/DAT/MBT_METING.dat': (30, 'meetbouten/MBT_METING.dat'),
    'meetbouten/DAT/MBT_REFERENTIEPUNT.dat': (30, 'meetbouten/MBT_REFERENTIEPUNT.dat'),
    'meetbouten/DAT/MBT_ROLLAAG.dat': (30, 'meetbouten/MBT_ROLLAAG.dat'),
    'nap/DAT/NAP_PEILMERK.dat': (30, 'nap/NAP_PEILMERK.dat'),
}


def fetch_gob_files(container_name, prefix):
    logging.basicConfig(level=logging.DEBUG)
    now = datetime.datetime.today()

    for file_object in get_full_container_list(
            'GOB_user', container_name, prefix=prefix):

        if file_object['content_type'] == 'application/directory':
            continue

        file_path = file_object['name']
        path = file_path.split('/')

        file_max_age_and_target = gob_file_age_and_target_list.get(file_path)
        file_name = path[-1]

        if not file_max_age_and_target:
            continue

        (file_max_age, file_target) = file_max_age_and_target
        file_last_modified = parser.parse(file_object['last_modified'])

        delta = now - file_last_modified
        log.debug('AGE %s: %2d days', file_name, delta.days)

        if delta.days > file_max_age:
            raise ValueError(f"""

            Delivery of file {file_name }is late!

            {file_path} age {delta.days} max_age: {file_max_age}
            """)

        directory = os.path.join(DIVA_DIR, *path[:-1])
        if not os.path.exists(directory):
            os.makedirs(directory)

        download_file('GOB_user', container_name, file_path, target_path=file_target,
                      file_last_modified=file_last_modified)


def unzip_data(zips_mapper):
    """
    unzip the zips
    """

    for _, zipfiles in zips_mapper.items():

        latestzip = zipfiles[0][1]

        filepath = latestzip['name'].split('/')
        file_name = filepath[-1]
        zip_path = '{}/{}'.format(DIVA_DIR, file_name)

        log.info(f"Unzip {zip_path}")

        zipsource = zipfile.ZipFile(zip_path, 'r')

        zip_date = file_name.split('_')[0]
        log.debug('DATE: %s', zip_date)
        zip_date = parser.parse(zip_date)
        zip_seconds = time.mktime(zip_date.timetuple())
        unzip_files(zipsource, zip_seconds)


def delete_from_objectstore(connect, container, object_name):
    """
    remove file `object_name` from `container`
    :param connect: Connection identifier
    :param container: Container name
    :param object_name:
    :return:
    """
    return get_conn(connect).delete_object(container, object_name)


def delete_old_zips(container_name, zips_mapper):
    """
    Cleanup old zips
    """
    for zipkey, zipfiles in zips_mapper.items():
        log.debug('KEEP : %s', zipfiles[0][1]['name'])
        if len(zipfiles) > 1:
            # delete old files
            for _, zipobject in zipfiles[1:]:
                zippath = zipobject['name']
                log.debug('PURGE: %s', zippath)
                delete_from_objectstore('bag_brk', container_name, zippath)


def fetch_diva_zips(container_name, zipfolder):
    log.info("import files from {}".format(zipfolder))

    zips_mapper = {}

    for file_object in get_full_container_list('bag_brk', container_name, prefix=zipfolder):

        if file_object['content_type'] == 'application/directory':
            continue

        path = file_object['name'].split('/')
        file_name = path[-1]

        if not file_name.endswith('.zip'):
            continue

        if not any(pattern in file_name for pattern in ['NAP', 'MBT']):
            continue

        dt = parser.parse(file_object['last_modified'])

        file_key = "".join(file_name.split('_')[1:])

        zips_mapper.setdefault(file_key, []).append((dt, file_object))

    download_zips(container_name, zips_mapper)
    delete_old_zips(container_name, zips_mapper)

    validate_age(zips_mapper)

    unzip_data(zips_mapper)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-g', '--gob', action='store_true', help='Do GOB import')
    args = argparser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    # Download files from objectstore
    log.info("Start downloading files from objectstore")
    if args.gob:
        fetch_gob_files('productie', 'meetbouten')
        fetch_gob_files('productie', 'nap')
    else:
        create_target_directories()
        fetch_diva_zips('Diva', 'Zip_bestanden')
    log.info("Finished downloading files from objectstore")
