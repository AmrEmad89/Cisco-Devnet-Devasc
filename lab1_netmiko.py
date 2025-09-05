#!/usr/bin/env python3
import getpass
import json
from netmiko import ConnectHandler


def get_router_configs(router_name, filename):
    """
    Retrieve configuration commands for a specific router.

    Args:
        router_name (str): Name of the router (e.g., "R1").
        filename (str): Path to JSON config file containing router commands.

    Returns:
        list: A list of CLI commands, or an empty list if router not found or file error.
    """
    try:
        with open(filename) as file:
            routers_configs = json.load(file)
            # Try to get the command list for the specified router
            router_config = routers_configs.get(router_name, [])
        if not router_config:
            print(f"[!] Router '{router_name}' not found in the config file.")
        return router_config
    except FileNotFoundError:
        print("[!] Configuration file not found.")
        return []
    except json.JSONDecodeError:
        print("[!] Error decoding JSON in the configuration file.")
        return []


def get_router_values(router_name, username, password, secret, routers_values_file):
    """
    Retrieve connection details for a specific router and insert credentials.

    Args:
        router_name (str): Name of the router (e.g., "R1").
        username (str): SSH username.
        password (str): SSH password.
        secret (str): Enable secret password.
        routers_values_file (str): Path to JSON file with base connection info.

    Returns:
        dict: Dictionary of connection parameters, or {} if router not found or file error.
    """
    try:
        with open(routers_values_file) as file:
            routers_values = json.load(file)
            router_values = routers_values[router_name]

            # Inject credentials into the router's connection parameters
            router_values["username"] = username
            router_values["password"] = password
            router_values["secret"] = secret

            return router_values
    except KeyError:
        print(f"[!] Router '{router_name}' not found in the values file.")
    except FileNotFoundError:
        print("[!] Router values file not found.")
    except json.JSONDecodeError:
        print("[!] Error decoding JSON in the router values file.")
    return {}


def connect_and_configure(routers, config_file, routers_values_file, username, password, secret):
    """
    Establish SSH connection to each router and push configuration commands.

    Args:
        routers (list): List of router names to configure.
        config_file (str): Path to JSON file with config commands per router.
        routers_values_file (str): Path to JSON file with SSH/IP/device_type per router.
        username (str): SSH username.
        password (str): SSH password.
        secret (str): Enable secret password.

    Returns:
        None
    """
    for router in routers:
        # Retrieve connection parameters for this router
        router_values = get_router_values(router, username, password, secret, routers_values_file)
        if not router_values:
            continue  # Skip if unable to get connection details

        # Retrieve CLI commands to send
        router_configs = get_router_configs(router, config_file)
        if not router_configs:
            continue  # Skip if no commands found

        try:
            print(f"\n[+] Connecting to {router}...")

            # Open SSH session using Netmiko
            with ConnectHandler(**router_values) as net_connect:
                net_connect.enable()  # Enter enable mode

                # Send configuration commands
                output = net_connect.send_config_set(router_configs)

                # Print config output
                print(f"[✔] Configuration applied to {router}:\n{output}")
        except Exception as e:
            print(f"[✗] Failed to connect to {router}: {e}")


if __name__ == "__main__":
    # Prompt user for routers to configure
    routers_input = input("Enter router names (comma-separated, e.g., R1,R2): ")
    routers = [r.strip() for r in routers_input.split(",")]

    # Prompt for config and values file paths
    config_file = input("Enter the config filename (e.g., routers_configs.txt): ")
    routers_values_file = input("Enter the router values filename (e.g., routers_values.txt): ")

    # Prompt for login credentials securely
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")
    secret = getpass.getpass("Enter your enable password: ")

    # Start configuration
    connect_and_configure(routers, "routers_configs.txt", "routers_values.txt", username, password, secret)
