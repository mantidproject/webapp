#! /bin/bash
# Starts the stack
set -e

function mk_django_secret() {
  python -c "import random,string;print 'SECRET_KEY=\"%s\"'%''.join([random.SystemRandom().choice(\"{}{}{}\".format(string.ascii_letters, string.digits, string.punctuation)) for i in range(63)])";
}

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)

COMPOSE_FILES="--file ${SOURCE_DIR}/docker-compose.yml --file ${SOURCE_DIR}/docker-compose-db-import.yml"
PROJECT_NAME=reports

# Required by django settings
DB_SERVICE=postgres
DB_PORT=5432
# Create a secret key
SECRET_KEY=$(mk_django_secret)
export DB_SERVICE DB_PORT SECRET_KEY

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
  echo "Usage: $0 path-to-postgres-sql-dump.sql"
  exit 1
fi

if [ ! -f ${SOURCE_DIR}/.env ]; then
  echo "Unable to find environment file ${SOURCE_DIR}/.env. It must contain the following variables:"
  echo "  DB_NAME, DB_USER, DB_PASS"
  exit 1
fi

# Build services
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} build
# Bring up the stack and detach
docker-compose ${COMPOSE_FILES} --project-name ${PROJECT_NAME} up -d
