#!/bin/bash

set -e
set -u

DIR="$(dirname $0)"

dc() {
	docker-compose -p nap -f ${DIR}/docker-compose.yml $*
}

trap 'dc kill ; dc down ; dc rm -f' EXIT

rm -rf ${DIR}/backups
mkdir -p ${DIR}/backups

echo "Building dockers"
dc down
dc pull
dc build

dc up -d database
dc up -d elasticsearch
dc run importer ./docker-wait.sh

echo "Starting Postgres and Elastic importer"
dc run --rm importer

echo "Running backups"
dc exec -T database backup-db.sh nap
dc exec -T elasticsearch backup-indices.sh meetbouten meetbouten
dc down -v
echo "Done"
