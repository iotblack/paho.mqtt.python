#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd ${BASEDIR}

PIDFILE="run/mosquitto.pid"

if [ -f "${PIDFILE}" ]
then
    kill -9 `cat ${PIDFILE}`
    echo "mosquitto killed trough ${PIDFILE}"
    rm -f ${PIDFILE}
else
    echo "mosquitto process not running"
fi

echo starting mosquitto 

mosquitto -c mosquitto.conf -d
sleep 1
if [ -f "${PIDFILE}" ]
then
    echo "start mosquitto success"
else
    echo "ERROR: mosquitto start failed"
fi


