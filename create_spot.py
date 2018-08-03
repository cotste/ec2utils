import boto3
import time

AMI = 'ami-f2d3638a'
INSTANCE_TYPE = 'm3.medium'
REGION = 'us-west-2'
KEYNAME = 'cotste-us-west-2'

ec2 = boto3.resource('ec2', region_name=REGION)

instance = ec2.create_instances(
        ImageId = AMI,
        InstanceType = INSTANCE_TYPE,
        KeyName= KEYNAME,
        MinCount = 1,
        MaxCount = 1,
        InstanceMarketOptions = {
            'MarketType' : 'spot',
            'SpotOptions' : {
                'SpotInstanceType' : 'one-time',
                'InstanceInterruptionBehavior' : 'terminate'
            }
        }

        )

instance.wait_until_running()

print( instance['InstanceId']) 
