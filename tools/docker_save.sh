#!/bin/bash

set -e
. version.sh

docker save osemmler/miio2mqtt:${VERSION} | gzip > osemmler_miio2mqtt_${VERSION}.tar.gz