import sys, os
#import spot_instance

def main_menu() :
    
    os.system('clear')
    print( 30 * '-', 'Main Menu', 30 * '-')
    print( '1. List Active Spot Instances')
    print( '2. Delete Spot Instances')
    print( '3. Create Spot Instances\n')

    choice = input('Choice: ')

    menu_choice = {
            '1' : list_spot_instances(),
            '2' : delete_spot_instances(),
            '3' : create_spot_instances()
    }

    result = menu_choice.get(choice, -1)

    #menu_func = main_opt(choice)

    #menu_func

def main_opt(selection) :
    selector = { 
            1 : list_spot_instances(),
            2 : delete_spot_instances(),
            3 : create_spot_instances()
    }


def list_spot_instances() :
    print('list_spot_instances() called\n')

def delete_spot_instances() :
    print('delete_spot_instances() called\n')

def create_spot_instances() :
    print('create_spot_instances() called\n')

main_menu()
