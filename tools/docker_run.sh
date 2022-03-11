#!/bin/bash

set -e
. version.sh

LOCAL_CONF=$(ls ${PWD}/../local_*.yaml | head -1)

docker run -v ${LOCAL_CONF}:/opt/miio2mqtt/config.yaml osemmler/miio2mqtt:${VERSION}
