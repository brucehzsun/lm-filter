#!/bin/bash

cd `dirname $0`

APP_NAME="lm-filter"
APP_VERSION="1.0"
IMG_TAG_NAME="${APP_NAME}:${APP_VERSION}"

echo "build docker image... [${IMG_TAG_NAME}]"
docker build -t $IMG_TAG_NAME .

#IMG_TAR_FILE="./${APP_NAME}-${APP_VERSION}.tar"
echo "DONE"
