import boto3
import sys
import os
import time
import argparse

import spot_instance as si

AMI = 'ami-f2d3638a'
INSTANCE_TYPE = 't3.large'
REGION = 'us-west-2'
KEYNAME = 'cotste-us-west-2'
COTSTE_ZONEID = 'Z35YLRGJE15KJD'

parser = argparse.ArgumentParser()
parser.add_argument( '-r', '--region', nargs='?', default=REGION, const=REGION)
parser.add_argument( '-a', '--ami', nargs='?', default=AMI, const=AMI)
parser.add_argument( '-i', '--instance_type', nargs='?', default=INSTANCE_TYPE, const=INSTANCE_TYPE)
parser.add_argument( '-k', '--keyname', nargs='?', default=KEYNAME, const=KEYNAME)

args = vars(parser.parse_args())

instance = si.create_spot(args['instance_type'], args['ami'], args['region'], args['keyname'])

#print('Instance created, instanceID: %s', mc_instance['InstanceId'])


mc_instance = instance[0]

time.sleep(10)

print('\n\nPublic IP: {0}\nPublic DNS: {1}\nHypervisor: {2}\nCPU Options: {3}\nInstance Type: {4}\n'.format(
    mc_instance.public_ip_address,
    mc_instance.public_dns_name,
    mc_instance.hypervisor,
    mc_instance.cpu_options,
    mc_instance.instance_type))

