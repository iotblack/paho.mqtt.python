#! /bin/bash
mosquitto_pub -t shadow/update -m '{"method":"get"}'

