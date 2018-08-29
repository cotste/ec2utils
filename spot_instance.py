import boto3
import sys
import argparse

AMI = 'ami-f2d3638a'
INSTANCE_TYPE = 't2.micro'
REGION = 'us-west-2'
KEYNAME = 'cotste-us-west-2'

parser = argparse.ArgumentParser()
parser.add_argument( '-r', '--region', nargs='?', default=REGION, const=REGION)
parser.add_argument( '-a', '--ami', nargs='?', default=AMI, const=AMI)
parser.add_argument( '-i', '--instance_type', nargs='?', default=INSTANCE_TYPE, const=INSTANCE_TYPE)
parser.add_argument( '-k', '--keyname', nargs='?', default=KEYNAME, const=KEYNAME)

args = vars(parser.parse_args())

#for a in args:
#    print(a, args[a])

#del_instance = sys.argv[1]

def delete_spot():

    #ec2 = boto3.resource( 'ec2', region_name=REGION)
    client = boto3.client( 'ec2', region_name=args['region'])

    print( 'Getting active spot instance requests...')

    response = client.describe_spot_instance_requests(
            Filters = [
                {
                    'Name' : 'state',
                    'Values' : [
                        'active'
                        ]
                    }
                ]
            )
                       
    num_reqs = len(response['SpotInstanceRequests'])

    print( 'There are currently ' + str(num_reqs ) + ' spot instance requests active')

    if num_reqs > 0 :
        
        req_num = 0
        for request in response['SpotInstanceRequests']:
            reqID = request['SpotInstanceRequestId']
            instID = request['InstanceId']
            print( 'This will cancel the following spot instance request and terminate the instance')
            print( "\nInstanceId: " + request['InstanceId'] 
                    + "\nState: " + request['State'] 
                    + '\nDate: ' + request['CreateTime'].strftime('%d-%B')
                    + '\nRequestID: ' + request['SpotInstanceRequestId'])

            cont = input( 'Would you like to continue with this action? (y/n) \n')
            if cont.lower() == 'y':

                print( 'Terminating instance with InstanceId: ' + request['InstanceId'])
                client.terminate_instances(
                     InstanceIds = [
                         instID
                         ]
                        )
                
                print( 'Cancelling spot request with RequestId: ' + reqID ) 
                reqResponse = client.cancel_spot_instance_requests(
                    SpotInstanceRequestIds = [
                        reqID
                        ]
                    )

                print( 'Response: ' 
                        + '\n\tRequest ID: ' + reqResponse['CancelledSpotInstanceRequests'][req_num]['SpotInstanceRequestId']
                        + '\n\tState: ' + reqResponse['CancelledSpotInstanceRequests'][req_num]['State'])
           
            elif cont.lower() == 'n':
                print( 'Cancelling, no action taken.')
            
            else :
                print( 'Invalid response')

    else :
        print('\nNo active spot requests found')
        exit(0)

def create_spot(instance_type, ami, region):
    
    import boto3
    import time

    ec2 = boto3.resource('ec2', region_name=region)

    instance = ec2.create_instances(
            ImageId = ami,
            InstanceType = instance_type,
            KeyName= keyname,
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

    #instance.wait_until_running()

    print( instance['InstanceId']) 

def list_spots():

    client = boto3.client( 'ec2', region_name=args['region'])

    print( 'Getting spot instance requests...')

    requests = client.describe_spot_instance_requests()

                       
    num_reqs = len(requests['SpotInstanceRequests'])

    print( 'There are currently ' + str(num_reqs ) + ' spot instance requests active')

    req_num = 0
    if num_reqs > 0:
        for request in requests['SpotInstanceRequests']:
            print('\n', 30 * '-', request['InstanceId'], 30 * '-')
            print( '\nInstanceId: ' + request['InstanceId'] 
                        + '\nState: ' + request['State'] 
                        + '\nDate: ' + request['CreateTime'].strftime('%d-%B')
                        + '\nRequestID: ' + request['SpotInstanceRequestId'])
            print(30 * '-', request['InstanceId'], 30 * '-')

def map_zones():

    r53client = boto3.client('route53')

    hzones = r53client.list_hosted_zones()

    #print(hzones)

    for hzone in hzones['HostedZones']:
        print('\n', 30 * '-', hzone['Id'], 30 * '-')
        print('Name: ', hzone['Name']
                + '\nResource Record Set Count: ', str(hzone['ResourceRecordSetCount'])
                + '\nPrivate Zone: ', hzone['Config']['PrivateZone'])
        print(30 * '-', hzone['Id'], 30 * '-')
list_spots()
map_zones()

