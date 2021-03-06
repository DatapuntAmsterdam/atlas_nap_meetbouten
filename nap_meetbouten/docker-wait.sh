#!/usr/bin/env bash

set -u
set -e

# wait for elastic
while ! nc -z elasticsearch 9200
do
	echo "Waiting for elastic..."
	sleep 2
done

# wait for postgres
while ! nc -z database 5432
do
	echo "Waiting for postgres..."
	sleep 2
done
