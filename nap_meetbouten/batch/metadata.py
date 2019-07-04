import datetime
import logging
import requests
import os

# TODO: shouldn't rely on an env variable here
METADATA_URL = os.getenv('METADATA_URL')

log = logging.getLogger(__name__)


def upload(dataset_id, year, month, day):
    # TODO: should fail if this method is called without having a URL
    if METADATA_URL is None or len(METADATA_URL) == 0:
        log.warning("METADATA_URL is not set, won't upload dataset modification "
                 "date. This should only happen during tests!")
        return

    metadata_url = METADATA_URL
    if metadata_url[-1] != '/':
        metadata_url += '/'

    try:
        dsid = dataset_id.lower()
    except AttributeError as e:
        log.critical("dataset_id cannot be lowercased. Is it a string?")
        raise e

    uri = '{}{}/'.format(metadata_url, dsid)

    try:
        moddate = '{}-{}-{}'.format(year, month, day)
        datetime.datetime.strptime(moddate, '%Y-%m-%d')
    except ValueError as e:
        log.critical("Could not parse date. Did you provide a valid year, "
                     "month and day?")
        raise e

    return requests.put(uri, {
        'id': dsid,
        'data_modified_date': moddate,
        'last_import_date': datetime.date.today(),
    })
