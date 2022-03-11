"""
MQTT client serving as a bridge between miio and mqtt broker.
"""

import signal
import os
import time
import inspect
import json
from functools import partial

import paho.mqtt.client as mqtt
import miio
from miio import *

from app import CONFIG, LOG

DEVICE_MAP = {}
MQTT_ID = CONFIG['mqtt']['client']['id']
MQTT_CLIENT = mqtt.Client(client_id=MQTT_ID)


def _add_device_to_device_map(name : str, address : str, token : str, model : str = None):

    if model is None:
        # get model of device
        LOG.info("try to determine model for device '%s' address '%s'", name, address)
        common_device = miio.Device(address,token)
        model = common_device.model

    # find class for model
    value = miio.discovery.DEVICE_MAP.get( model.replace('.', '-') )

    if value is None:
        LOG.error("can not find class for model '%s' in miio.discovery.DEVICE_MAP", model)
        LOG.info("miio.discovery.DEVICE_MAP = %s", miio.discovery.DEVICE_MAP.keys())

    elif inspect.isclass(value):
        device_object = value(address,token)
        DEVICE_MAP[name] = device_object
        LOG.info("device created: name '%s' model '%s' address '%s'", name, model, address)

    elif isinstance(value, partial) and inspect.isclass(value.func):
        raise NotImplementedError

    else:
        LOG.error("can not create device: name '%s' model '%s' address '%s'", name, model, address)


def _create_device_map():
    for device in CONFIG['devices']:
        name = device['name']
        _add_device_to_device_map(name, device['ip'], device["token"], device.get("model"))

        qos = CONFIG['mqtt']['subscribe']['qos']
        MQTT_CLIENT.subscribe(f"{MQTT_ID}/{name}/cmd/#", qos)


def _send_device_status_data(name):
    try:
        device = DEVICE_MAP[name]
        status_data = device.status()
        json_object = json.dumps(status_data.data)
        topic = f"{MQTT_ID}/{name}"
        LOG.info("mqtt publish %s = %s", topic, json_object)

        qos = CONFIG['mqtt']['publish']['qos']
        retain = CONFIG['mqtt']['publish']['retain']
        MQTT_CLIENT.publish(topic, json_object, qos, retain)

    except miio.exceptions.DeviceException as exception:
        LOG.error("device '%s' error: %s", name, exception)


def _send_status_data():
    for name in DEVICE_MAP:
        _send_device_status_data(name)


def _mqtt_on_connect(client, userdata, flags, result_code):
    del client, userdata, flags
    LOG.info("mqtt broker connected with result code: %i", result_code)
    if result_code != 0:
        LOG.error("can not connect to mqtt broker - app will exit now")
        os._exit(1)

    MQTT_CLIENT.publish(f"{MQTT_ID}/status","ONLINE",1,True)


def _mqtt_on_disconnect(client, userdata, flags, result_code):
    del client, userdata, flags
    LOG.info("mqtt broker disconnected with result code: %i", result_code)
    MQTT_CLIENT.publish(f"{MQTT_ID}/status","OFFLINE",1,True)


def _mqtt_on_message(client, userdata, msg):
    del client, userdata
    LOG.info("incomming mqtt message '%s = %s'", msg.topic, msg.payload)

    try:
        topic_list = msg.topic.split('/')

        if topic_list[0] == MQTT_ID :
            name = topic_list[1]

            if topic_list[2] == 'cmd' :
                cmd = topic_list[3]
                args = msg.payload.decode("utf-8")

                exec_str = f"DEVICE_MAP[name].{cmd}({args})"
                output = exec(exec_str)
                LOG.info("device '%s' exec '%s' output: %s", name, exec_str, output)
                _send_device_status_data(name)

    except miio.exceptions.DeviceException as exception:
        LOG.error("DeviceException device '%s' error: %s", name, exception)

    except AttributeError as exception:
        LOG.error("AttributeError device '%s' error: %s", name, exception)

    except TypeError as exception:
        LOG.error("TypeError device '%s' error: %s", name, exception)


def start():
    """
    Start the MQTT client.
    """

    if 'auth' in CONFIG['mqtt']:
        LOG.info("mqtt using username:password authentication")
        username = CONFIG['mqtt']['auth']['username']
        password = CONFIG['mqtt']['auth']['password']
        MQTT_CLIENT.username_pw_set(username, password)

    address = CONFIG['mqtt']['host']['address']
    port = CONFIG['mqtt']['host']['port']
    keepalive = CONFIG['mqtt']['host']['keepalive']

    MQTT_CLIENT.will_set(f"{MQTT_ID}/status","DISCONNECTED",1,True)
    MQTT_CLIENT.on_connect = _mqtt_on_connect
    MQTT_CLIENT.on_disconnect = _mqtt_on_disconnect
    MQTT_CLIENT.on_message = _mqtt_on_message
    MQTT_CLIENT.connect(address, port, keepalive)
    MQTT_CLIENT.loop_start()

    _create_device_map()

    idle = CONFIG['system']['idle']
    while True:
        _send_status_data()
        LOG.info("idle %i s", idle)
        time.sleep(idle)


if __name__ == '__main__':
    raise NotImplementedError("Run 'run.py' to start application.")
