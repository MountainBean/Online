#!/bin/bash

METADATATOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
INTERFACE_MAC=`curl http://169.254.169.254/latest/meta-data/mac -H "X-aws-ec2-metadata-token: $METADATATOKEN"`
PUBLIC_IP=`curl http://169.254.169.254/latest/meta-data/network/interfaces/macs/$INTERFACE_MAC/public-ipv4s -H "X-aws-ec2-metadata-token: $METADATATOKEN"`
DJ_SECRET_KEY=

cat <<EOT >> change_batch.json
{
    "Comment": "UPSERT website record ",
    "Changes": [{
    "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": "mountainbean.online",
            "Type": "A",
            "TTL": 300,
            "ResourceRecords": [{ "Value": "$PUBLIC_IP"}]
}}]
}
EOT
aws route53 change-resource-record-sets --hosted-zone-id Z08242151MWOY90HMWF69 --change-batch file://change_batch.json
sudo rm change_batch.json

sudo groupadd www-data

cd /home/ec2-user

aws s3api get-object\
 --bucket website-source-packages-github-actions-upload \
 --key `aws s3api list-objects --bucket website-source-packages-github-actions-upload | jq -r '.Contents[].Key | select( endswith("latest") )'`\
 appfiles.zip

unzip appfiles.zip -d Website

sudo dnf upgrade
sudo dnf install python3.11 nginx -y

cd Website

python3.11 -m venv .venv
. ./.venv/bin/activate

python3.11 -m pip install -r requirements.txt
deactivate

cat <<EOT >> gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ec2-user
Group=www-data
WorkingDirectory=/home/ec2-user/Website
ExecStart=/home/ec2-user/Website/.venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 1 \\
          --threads 15 \\
          --bind unix:/run/gunicorn.sock \\
          Online.wsgi:application \\
          --env DJANGO_WEBSITE_ENVIRONMENT=PROD \\
          --env DJ_SECRET_KEY=$DJ_SECRET_KEY \\

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT >> gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOT

sudo cp gunicorn.{socket,service} /etc/systemd/system/
sudo cp .ec2config/nginx.conf /etc/nginx/conf.d/Online.conf


sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl restart nginx

sudo python3.11 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip

sudo /opt/certbot/bin/pip install certbot certbot-nginx

sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
sudo certbot --nginx -d mountainbean.online -n --agree-tos --email sambo2@live.com.au
