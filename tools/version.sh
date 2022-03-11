export VERSION=$(git -C . describe --dirty | sed 's/^v//')
echo "MIIO2MQTT_VERSION='${VERSION}'" > ../script/version.py