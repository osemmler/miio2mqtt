#!/bin/bash

set -e
. version.sh

cd ..
docker build --tag osemmler/miio2mqtt:${VERSION} --tag osemmler/miio2mqtt:latest .