#! /bin/bash
# Starts the stack
set -ex

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)

COMPOSE_FILES="--file ${SOURCE_DIR}/docker-compose.yml --file ${SOURCE_DIR}/docker-compose-db-import.yml"
PROJECT_NAME=reports

if [ $# -eq 1 ]; then
  if [ ! -f "$1" ]; then
    echo "SQL dump \"$1\" does not exist"
    exit 1
  fi
  DB_DUMP=$1
  if [ "${DB_DUMP:0:1}" != "/" ]; then
      DB_DUMP=$PWD/$DB_DUMP
  fi
  export DB_DUMP
else
  echo "Usage: $0 path-to-sql-dump.sql"
  exit 1
fi

if [ ! -f ${SOURCE_DIR}/.env ]; then
  echo "Unable to find environment file ${SOURCE_DIR}/.env. It must contain the following variables:"
  echo "  DB_NAME, DB_USER, DB_PASS, SECRET_KEY, DB_SERVICE, DB_PORT"
  exit 1
fi

# Build services
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} build
# Bring up the stack and detach
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} up -d
