import boto3
import sys

REGION = 'us-west-2'
#del_instance = sys.argv[1]

ec2 = boto3.resource( 'ec2', region_name=REGION)
client = boto3.client( 'ec2', region_name=REGION)

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
    for request in response['SpotInstanceRequests']:
        reqID = request['SpotInstanceRequestId']
        instID = request['InstanceId']
        print( 'This will cancel the following spot instance request and terminate the instance')
        print( "\nInstanceId: " + request['InstanceId'] 
                + "\nState: " + request['State'] 
                + '\nDate: ' + request['CreateTime'].strftime('%d-%B')
                + '\nRequestID: ' + request['SpotInstanceRequestId'])

        cont = input( 'Would you like to continue with this action? (y/n) \n')
        if cont == 'y':

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

            print( 'Response: \n' + reqResponse['CancelledSpotInstanceRequests'][0]['State'])
       
        elif cont == 'n':
            print( 'OK')
        
        else :
            print( 'Invalid response')

else : exit(0)
