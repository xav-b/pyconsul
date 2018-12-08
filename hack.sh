#!/usr/bin/env bash

set -o errexit
set -u nounset
set -o pipefail

echo "starting up containers"
docker-compose up -d
docker-compose ps

echo "entering dev box"
docker exec -it pyconsul_lab_1 bash
