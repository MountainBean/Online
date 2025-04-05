import subprocess
import json
import time

ip_addrs = json.loads(subprocess.run(['aws', 'ec2', 'describe-instances', '--query', 'Reservations[].Instances[].NetworkInterfaces[0].PrivateIpAddress'], capture_output=True).stdout.decode())
if len(ip_addrs) > 1:
    time.sleep(45)
    print("true")
else:
    print("false")
