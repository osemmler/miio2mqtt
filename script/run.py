""" The main sctript that runs the application.

The application requires the existence of a yaml configuration file. The path to
the file is defined by the environment variable 'MIIO2MQTT_CONFIG'. If the
variable 'MIIO2MQTT_CONFIG' is not defined, the configuration file is searched
for on the path '${PWD}/config/config.yaml'
"""

from app import CONFIG, LOG, VERSION
import client

if __name__ == '__main__':
    LOG.info("miio2mqtt version: '%s' started with config: %s", VERSION, CONFIG)
    client.start()
