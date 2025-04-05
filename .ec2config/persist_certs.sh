#!bin/bash

while [ $(python3 spot_monitor.py) != "true" ]
do
        sleep 5
done

# get new instance IP
NEW_INSTANCE_IPv4=$(aws ec2 describe-instances --query 'Reservations[].Instances[].{LaunchTime:LaunchTime,IPv4:NetworkInterfaces[0].PrivateIpAddress}' | jq -r "sort_by(.LaunchTime)| reverse | .[0].IPv4")
echo "DEBUG: NEW_INSTANCEIP: $NEW_INSTANCE_IPv4";

# Copy ssh key to new instance
sudo scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "/etc/ssh/launch template in console.pem" "/etc/ssh/launch template in console.pem" ec2-user@$NEW_INSTANCE_IPv4:~

# Copy certs to new instance
sudo rsync -Wav -e "ssh -o StrictHostKeyChecking=no -i \"/etc/ssh/launch template in console.pem\"" --progress /etc/letsencrypt/ ec2-user@$NEW_INSTANCE_IPv4:letsencrypt

# SSH to new instance
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "/etc/ssh/launch template in console.pem" ec2-user@$NEW_INSTANCE_IPv4 -t 'sudo chmod 700 "launch template in console.pem" &&
sudo mv "launch template in console.pem" /etc/ssh/ &&
sudo chown -R root:root letsencrypt &&
sudo rm -rf /etc/letsencrypt &&
sudo mv letsencrypt /etc'

# check for renewal
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i "/etc/ssh/launch template in console.pem" ec2-user@$NEW_INSTANCE_IPv4 -t 'sudo certbot certificates &&
sudo certbot renew'
