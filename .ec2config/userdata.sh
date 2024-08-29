#!/bin/bash

METADATATOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
INTERFACE_MAC=`curl http://169.254.169.254/latest/meta-data/mac -H "X-aws-ec2-metadata-token: $METADATATOKEN"`
PUBLIC_IP=`curl http://169.254.169.254/latest/meta-data/network/interfaces/macs/$INTERFACE_MAC/public-ipv4s -H "X-aws-ec2-metadata-token: $METADATATOKEN"`

cat <<EOT >> change_batch.json
{
    "Comment": "UPSERT website record ",
    "Changes": [{
    "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "spot.mountainbean.online",
            "Type": "A",
            "TTL": 300,
            "ResourceRecords": [{ "Value": "$PUBLIC_IP"}]
}}]
}
EOT
aws route53 change-resource-record-sets --hosted-zone-id Z08242151MWOY90HMWF69 --change-batch file://change_batch.json

aws s3api get-object\
 --bucket website-source-artifacts-manual-in-console\
 --key `aws s3api list-objects --bucket website-source-artifacts-manual-in-console | jq -r '.Contents[].Key | select( endswith("latest") )'`\
 appfiles.zip

unzip appfiles.zip -d Website

sudo dnf upgrade
sudo dnf install python3.11 nginx -y

cd Website

python3.11 -m venv .venv
. ./.venv/bin/activate

python3.11 -m pip install -r requirements.txt

sudo adduser server
sudo groupadd www-data

sudo cp .ec2config/gunicorn.{socket,service} /etc/systemd/system/
chown www-data:www-data /etc/systemd/system/gunicorn.service
chown www-data:www-data /etc/systemd/system/gunicorn.socket
chown www-data:www-data -R Website/


sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket





