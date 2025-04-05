import datetime
import json
import requests

token = requests.put('http://169.254.169.254/latest/api/token', headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'})
interrupt = requests.get('http://169.254.169.254/latest/meta-data/spot/instance-action', headers={'X-aws-ec2-metadata-token': token.text})

if interrupt:
    inter_obj = json.loads(interrupt.text)
    end_time = datetime.datetime.strptime(inter_obj["time"], "%Y-%m-%dT%H:%M:%SZ")
    remaining = end_time - datetime.datetime.now()
    if remaining.seconds < 60:
        print("true")
else:
    print("false")
