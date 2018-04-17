cakeyfile=ca.key
cacrtfile=ca.crt

if [ -f "$cakeyfile" ]
then
    echo "$cakeyfile exist, please rename or move it away."
    exit 0
fi

if [ -f "$cacrtfile" ]
then
    echo "$cacrtfile exist, please rename or move it away."
    exit 0
fi

subj="/C=CN/ST=ShenZhen/L=ShenZhen/O=Example CA Inc./OU=Web Security/CN=ca.iot.test.local"
openssl req -new -x509 -days 3650 -extensions v3_ca -keyout $cakeyfile -out $cacrtfile -subj "$subj"



