#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows an example of an MQTT client that clears all of the retained messages it receives.

import sys
import getopt
import json

import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

gettopic = None
updatetopic = None

iot_storage = {}
iot_storage["shadow"] = {}
iot_storage["firm"] = {}

def on_connect(mqttc, userdata, flags, rc):
    if userdata == True:
        print("rc: " + str(rc))

def is_json(myjson):
    try:
      json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True


def on_message(mqttc, userdata, msg):
    global updatetopic
    global iot_storage
    print("received topic:" + msg.topic + "|" + msg.payload)
    if not is_json(msg.payload):
        print("invalid payload:" + msg.payload)
        return

    req = json.loads(msg.payload.decode("utf-8"))
    resp = {}
    resp["method"]= "reply"
    resp["passthrough"] = req['passthrough']
    if req["method"] == "get":
        resp['state'] = iot_storage["shadow"]
        resp_str = json.dumps(resp)
        print("response:" + resp_str)
        mqttc.publish(gettopic, resp_str, 1, True)
    elif req["method"] == "update":
        if "reported" in req["state"]:
            for k in req["state"]["reported"]:
                iot_storage["shadow"]["reported"][k] = req["state"]["reported"][k]
                #  print("report : " + k + "=", v)
        if "desired" in req["state"]:
            for k in req["state"]["desired"]:
                iot_storage["shadow"]["desired"][k] = req["state"]["desired"][k]
                #  print("desired : " + k + "=", v)

        resp_str = json.dumps(resp)
        print("response:" + resp_str)
        mqttc.publish(gettopic, resp_str, 1, True)
        #  mqttc.publish(gettopic, '{"method":"control"}', 1, True)
    elif req["method"] == "update_firm_info":
        iot_storage["firm"] = req["state"]
        resp_str = json.dumps(resp)
        print("response:" + resp_str)
        mqttc.publish(gettopic, resp_str, 1, True)
    else :
        print("invalid method:" + req["method"])


def on_publish(mqttc, userdata, mid):
    print("on_publish called");


def on_log(mqttc, userdata, level, string):
    print(string)


def print_usage():
    print(
        "shadow.py [-d] [-h hostname] [-i clientid] [-k keepalive] [-p port] [-u username [-P password]] [-v] -t topic")


def main(argv):
    global gettopic
    global updatetopic

    debug = False
    host = "localhost"
    client_id = None
    keepalive = 60
    port = 1883
    password = None
    username = None
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "dh:i:k:p:P:T:U:u:v",
                                   ["debug", "id", "keepalive", "port", "password",
                                    "gettopic", "updatetopic", "username", "verbose"])
    except getopt.GetoptError as s:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-i", "--id"):
            client_id = arg
        elif opt in ("-k", "--keepalive"):
            keepalive = int(arg)
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-P", "--password"):
            password = arg
        elif opt in ("-T", "--gettopic"):
            gettopic = arg
            print(gettopic)
        elif opt in ("-U", "--updatetopic"):
            updatetopic = arg
            print(updatetopic)
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    if updatetopic == None:
        print("You must provide a upodatetopic.\n")
        print_usage()
        sys.exit(2)

    if gettopic == None:
        print("You must provide a gettopic.\n")
        print_usage()
        sys.exit(2)

    mqttc = mqtt.Client(client_id)
    mqttc._userdata = verbose
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    if debug:
        mqttc.on_log = on_log

    if username:
        mqttc.username_pw_set(username, password)
    mqttc.connect(host, port, keepalive)
    mqttc.subscribe(updatetopic)
    mqttc.loop_forever()


if __name__ == "__main__":
    main(sys.argv[1:])
