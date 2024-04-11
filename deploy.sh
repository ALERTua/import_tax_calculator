#!/bin/bash
IMAGE_NAME=import_tax_calc
IMAGE_TAG=latest
IMAGE_STAGE=production

LOCAL_IMAGE_TAG=$IMAGE_NAME:$IMAGE_TAG
BUILD_PATH=.
# shellcheck disable=SC2034
DOCKER_BUILDKIT=1

test -f poetry.lock || (echo "poetry.lock not found" & exit)

docker build -t $LOCAL_IMAGE_TAG $BUILD_PATH --target=$IMAGE_STAGE || exit

# docker push $REMOTE_IMAGE_TAG
