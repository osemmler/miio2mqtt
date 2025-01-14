# Miio2MQTT

Miio2MQTT is a two-way bridge between **Xiaomi protocols (miIO and MIoT)** and **MQTT**.

The bridge is implemented as an MQTT client that reads data from Xiaomi devices at regular intervals and sends them to the MQTT broker.

The bridge also accepts commands from the MQTT broker for Xiaomi devices (on, off, set parameter, etc.).

# Getting started

The bridge is primarily distributed as a **Docker image**. The complete bridge setup is defined in a **YAML configuration file**.

1) Create YAML configuration file

    - Download default *config.yaml*: https://github.com/osemmler/mybin/blob/master/config.yaml

    - Open *config.yaml* file and edit it according to the instructions in the comments.

2) Run Docker image

    ```bash
    docker run -v ${PWD}/config.yaml:/opt/miio2mqtt/config.yaml osemmler/miio2mqtt:latest
    ```

3) The bridge should now send data to the MQTT broker. You can see the details of the communication in the log.

# Troubleshooting

**I don't have an MQTT broker yet.**
- Use Eclipse Mosquitto MQTT broker
    - Home page https://mosquitto.org/
    - Docker image https://hub.docker.com/_/eclipse-mosquitto


**How can I view data in MQTT broker?**
- Use MQTT Explorer
    - Home page http://mqtt-explorer.com/

# Architecture

Used libraries:
- Xiaomi protocols : python-miio https://github.com/rytilahti/python-miio
- MQTT client : paho-mqtt https://github.com/eclipse/paho.mqtt.python

Communication:
- miio -> MQTT:
    - Xiaomi device ---> [ python-miio >>> JSON Data >>> paho-mqtt ] ---> MQTT broker
    - Example of MQTT message with data readed from Xiaomi  device:
        ```json
        miio2mqtt/vacuum = {"msg_ver": 3, "msg_seq": 1081, "state": 8, "battery": 100, "clean_time": 2571, "clean_area": 53337500, "error_code": 0, "map_present": 1, "in_cleaning": 0, "in_returning": 0, "in_fresh_state": 1, "lab_status": 1, "water_box_status": 0, "fan_power": 104, "dnd_enabled": 0, "map_status": 3, "lock_status": 0}
        ```

- MQTT -> miio:
    - MQTT broker ---> [ paho-mqtt >>> cmd exec >>> python-miio ] ---> Xiaomi device
    - Miio2MQTT defines a special topic `cmd` for each Xiaomi device. This sub-topic is used for sending commands to that device.
    - Example commands:
      | MQTT topic with incoming data from Xiaomi device | Action | MQTT topic | MQTT topic value |
      | --------          | -------            | -------            | -------            |
      | miio2mqtt/vacuum  | Find vacuum cleaner  | miio2mqtt/vacuum/cmd/find | |
      | miio2mqtt/hum  | Power on humidifier | miio2mqtt/hum/cmd/on | |
      | miio2mqtt/hum  | Change mode of humidifier | miio2mqtt/hum/cmd/set_property | "mode", 2 |

# TODO List

- support miio.discovery module to automatically add new devices

# Links

Docker Hub: https://hub.docker.com/repository/docker/osemmler/miio2mqtt
