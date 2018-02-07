
subj="/C=CN/ST=ShenZhen/L=ShenZhen/O=Example MQTT Server Inc./OU=Web Security/CN=mqtt.iot.test.local"

openssl genrsa -out server.key 2048
openssl req -out server.csr -key server.key -new -subj "$subj"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650


