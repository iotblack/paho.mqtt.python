#! /bin/bash
product_id="iot-fdxt0fie"
device_name="light001"
python shadow.py -T shadow/get/$product_id/$device_name -U shadow/update/$product_id/$device_name

