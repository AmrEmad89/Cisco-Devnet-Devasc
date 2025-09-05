#!/usr/bin/env python3
import getpass
import json
#rom netmiko import ConnectHandler



def get_router_configs(router_name):
    
    """
    Fetch the configuration commands for a given router name from 'routers_configs.txt'.

    Args:
        router_name (str): The name of the router.

    Returns:
        list: A list of configuration commands or an empty list if not found.
    """
    # open the config file and load the content
    try:
        with open("routers_configs.txt") as file:
            routers_configs = json.load(file)  
            # return the list of commands for the given router name   
            router_config= routers_configs.get(router_name, [])
        if not router_config:
            print(f"Router {router_name} not found in the config file.")
        return router_config
    except FileNotFoundError:
        print("Configuration file not found.")
        return []
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON from the configuration file.")
        return []

# Function to get router connection values from a routers values file
# and update with provided username, password, and secret
        
def get_router_values(router_name,username,password,secret):
    # open the routers file and load the content
    with open("routers_vlaues.txt") as file:
        file_content = file.read()
        routers_values = json.loads(file_content)  
        # Check if the router name exists in the file and changes the username and password   
        try:
            router_values= routers_values[router_name]
            router_values["password"]=password
            router_values["username"]=username
            router_values["secret"]=secret
        except: 
            print(f"Router {router_name} not found in the values file.")
            return {}
        return router_values 
           



def connect_and_configure(routers):
    # Loop through routers dict: {router_name: connection_dict}
    for router in routers:
        router_values = get_router_vlaues(router)   
        router_configs = get_router_configs(router)
        # Check router reachability
        try :
            print(f"Connecting to {router_name}")
            # connect to the router 
            with ConnectHandler(**router_values) as net_connect:
                net_connect.enable()
                output = net_connect.send_config_set(router_configs)
                print("=== CONFIGURATION OUTPUT ===")
                print(output)
        except Exception as e:
            print(f"Failed to connect to {router_name}: {e}")

if __name__ == "__main__":
    
    # router_name = input("Enter the router name (e.g., router1): ")
    # username = input("Enter your SSH username: ")
    # password = getpass.getpass("Enter your SSH password: ")
    # secret = getpass.getpass("Enter your enable password: ")

    print(get_router_configs("R6"))