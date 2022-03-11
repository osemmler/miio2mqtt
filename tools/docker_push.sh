#!/bin/bash

set -e
. version.sh

docker push osemmler/miio2mqtt:${VERSION}
docker push osemmler/miio2mqtt:latest
