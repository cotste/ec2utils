import boto3
import sys
import os
import time
import argparse

import spot_instance as si

AMI = 'ami-6cd6f714'
#AMI = 'ami-f2d3638a'
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


#init_script = """#!/bin/bash
#    sudo /usr/bin/yum -y update
#    sudo /usr/bin/yum -y install java-1.8.0-openjdk tmux htop
#    sudo /usr/bin/yum -y remove java-1.7.0-openjdk
#    sudo /usr/bin/mkdir -p /srv/minecraft/
#    sudo /sbin/groupadd minecraft
#    sudo /sbin/useradd -s /bin/bash -c "Minecraft Server User" --system -d /srv/minecraft -g minecraft minecraft
#    echo 'minecraft:M!necr@ftPW!' | sudo chpasswd
#    /usr/bin/aws s3 cp s3://minecrafts3.cotste.com/zucoland-survival.tar.xz /srv/minecraft/
#    sudo /usr/bin/tar -xJvf /srv/minecraft/zucoland-survival.tar.xz -C /srv/minecraft/
#    sudo /usr/bin/cp /srv/minecraft/zucoland-survival/minecraft@.service /etc/systemd/system/
#    sudo /bin/chmod 664 /etc/systemd/system/minecraft@.service
#    sudo /bin/chown -R minecraft:minecraft /srv/minecraft
#    sudo /usr/bin/systemctl enable minecraft@zucoland-survival
#    sudo /usr/bin/systemctl start minecraft@zucoland-survival"""

init_script = """#!/bin/bash
    sudo /usr/bin/yum -y update"""

instance = si.create_spot(args['instance_type'], args['ami'], args['region'], args['keyname'], init_script)

#print('Instance created, instanceID: %s', mc_instance['InstanceId'])


mc_instance = si.get_instance(instance[0].instance_id)

mc_instance.wait_until_running()
mc_instance.load()

print('\n\nPublic IP: {0}\nPublic DNS: {1}\nHypervisor: {2}\nCPU Options: {3}\nInstance Type: {4}\n'.format(
    mc_instance.public_ip_address,
    mc_instance.public_dns_name,
    mc_instance.hypervisor,
    mc_instance.cpu_options,
    mc_instance.instance_type))

si.map_zones('zucoapoc.cotste.com', mc_instance.public_ip_address)



