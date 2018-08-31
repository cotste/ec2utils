import sys, os, argparse
import spot_instance as si

AMI = 'ami-f2d3638a'
INSTANCE_TYPE = 't2.micro'
REGION = 'us-west-2'
KEYNAME = 'cotste-us-west-2'
COTSTE_ZONEID = 'Z35YLRGJE15KJD'

parser = argparse.ArgumentParser()
parser.add_argument( '-r', '--region', nargs='?', default=REGION, const=REGION)
parser.add_argument( '-a', '--ami', nargs='?', default=AMI, const=AMI)
parser.add_argument( '-i', '--instance_type', nargs='?', default=INSTANCE_TYPE, const=INSTANCE_TYPE)
parser.add_argument( '-k', '--keyname', nargs='?', default=KEYNAME, const=KEYNAME)

args = vars(parser.parse_args())

def main_menu() :
    
    os.system('clear')
    print( 30 * '-', 'Main Menu', 30 * '-')
    print( '1. List Active Spot Instances')
    print( '2. Delete Spot Instances')
    print( '3. Create Spot Instances\n')

    choice = input('Choice: ')

    menu_choice = {
            '1' : list_spot_instances,
            '2' : delete_spot_instances,
            '3' : create_spot_instances
    }

    result = menu_choice.get(choice)()


    #menu_func = main_opt(choice)

def main_opt(selection) :
    selector = { 
            '1' : list_spots_instances,
            '2' : list_zones,
            '3' : delete_spot,
            '4' : create_spot
    }


def list_spot_instances() :
    
    results = si.list_spots(args['region'])

    num_reqs = len(results['SpotInstanceRequests'])
    req_num = 2

    inst_menu = {'1' : main_menu}
    

    for result in results['SpotInstanceRequests']:
        inst_menu[str(req_num)] = result['InstanceId']
        req_num += 1

    for key, value in inst_menu.items():
        print('{0}. {1}'.format(key, str(value)))


def delete_spot_instances() :
    print('delete_spot_instances() called\n')

def create_spot_instances() :
    print('create_spot_instances() called\n')

main_menu()
