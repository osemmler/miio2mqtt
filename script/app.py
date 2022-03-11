"""
Global variables and application configuration.
"""

import os
import logging
import importlib.util
import yaml

def _read_config() -> dict:
    """ Read configuration file.

    Reading the yaml configuration file into the dict structure. The content of
    the read file is checked while the program is running by querying the
    individual setting values.
    """

    yaml_config_file_name = os.environ.get('MIIO2MQTT_CONFIG')

    if not yaml_config_file_name:
        yaml_config_file_name = 'config.yaml'

    with open(yaml_config_file_name, "r", encoding="UTF-8") as config_file:
        return yaml.safe_load(config_file)


def _create_logger() -> logging.Logger:
    """ Creating a logger for application logging. """

    fmt = logging.Formatter('%(asctime)s %(levelname)s : %(message)s')

    logger = logging.getLogger('miio2mqtt_logger')
    logger.setLevel( logging.getLevelName('INFO') )

    if CONFIG['log']['to_file'] is True:
        file_handler = logging.FileHandler(CONFIG['log']['file_path'])
        file_handler.setFormatter(fmt)
        logger.addHandler( file_handler )

    if CONFIG['log']['to_console'] is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt)
        logger.addHandler( stream_handler )

    return logger


def _get_version() -> str:
    """ Try to get application version from version module. """

    if importlib.util.find_spec('version') is None:
        return "unknown"

    import version
    return version.MIIO2MQTT_VERSION


CONFIG = _read_config()
LOG = _create_logger()
VERSION = _get_version()


if __name__ == '__main__':
    raise NotImplementedError("Run 'run.py' to start application.")
