#! /bin/bash
# Stops the stack of containers and removes the _webdata container
# as it contains only non-persistent data.

SCRIPTPATH=$(cd "$(dirname "$0")"; pwd -P)
SOURCE_DIR=$(cd "$SCRIPTPATH" && cd .. && pwd -P)
PROJECT_NAME=reports

cd ${SOURCE_DIR}
docker-compose down
# The webdata should not really be a volume as all of the files come out of the image
# We remove it so the next rebuild sees the most recent version of the Python code
docker volume rm ${PROJECT_NAME}_webdata
