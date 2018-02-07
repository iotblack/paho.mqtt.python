
subj="/C=CN/ST=ShenZhen/L=ShenZhen/O=Example MQTT Client Inc./OU=Web Security/CN=client.iot.test.local"

openssl genrsa -out client.key 2048
openssl req -out client.csr -key client.key -new -subj "$subj"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365


