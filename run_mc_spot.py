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

init_script = """#!/bin/bash
    sudo yum -y update
    sudo yum -y install java-1.8.0-openjdk tmux htop
    sudo yum -y remove java-1.7.0-openjdk
    sudo mkdir /srv/minecraft
    sudo chown ec2-user:ec2-user /srv/minecraft"""
    

instance = si.create_spot(args['instance_type'], args['ami'], args['region'], args['keyname'], init_script)

#print('Instance created, instanceID: %s', mc_instance['InstanceId'])


mc_instance = instance[0]

time.sleep(10)

print('\n\nPublic IP: {0}\nPublic DNS: {1}\nHypervisor: {2}\nCPU Options: {3}\nInstance Type: {4}\n'.format(
    mc_instance.public_ip_address,
    mc_instance.public_dns_name,
    mc_instance.hypervisor,
    mc_instance.cpu_options,
    mc_instance.instance_type))

