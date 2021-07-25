#!/bin/bash
set -o allexport; source .env; set +o allexport

mosquitto_sub -d \
    -u ${OWNTRACKS_HTTP_MQTT_USER} \
    -P ${OWNTRACKS_HTTP_MQTT_PASSWORD} \
    -p ${OWNTRACKS_HTTP_MQTT_PORT} \
    -h ${OWNTRACKS_HTTP_MQTT_HOST} \
    -t 'owntracks/#' \
    --capath /etc/ssl/certs/