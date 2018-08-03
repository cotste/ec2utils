import boto3
import sys

REGION = 'us-west-2'
#del_instance = sys.argv[1]

def delete_spot() :

    #ec2 = boto3.resource( 'ec2', region_name=REGION)
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

