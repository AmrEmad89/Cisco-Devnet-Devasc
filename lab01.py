from netmiko import ConnectHandler
from getpass import getpass

ip_addresses={"R1":"192.168.122.11","R2":"192.168.122.12","R3":"192.168.122.13" }
routers_config= {

     'R1': [
            'interface Loopback0',
            'ip address 192.168.255.1 255.255.255.255',
            'interface GigabitEthernet2',
            'ip address 10.1.2.1 255.255.255.0',
            'interface GigabitEthernet3',
            'ip address 10.1.3.1 255.255.255.0',
            'router ospf 1',
            'network 0.0.0.0 255.255.255.255 area 0'
        ],
        'R2': [
            'interface Loopback0',
            'ip address 192.168.255.2 255.255.255.255',
            'interface GigabitEthernet2',
            'ip address 10.1.2.2 255.255.255.0',
            'interface GigabitEthernet3',
            'ip address 10.2.3.2 255.255.255.0',
            'router ospf 1',
            'network 0.0.0.0 255.255.255.255 area 0'
        ],
        'R3': [
            'interface Loopback0',
            'ip address 192.168.255.3 255.255.255.255',
            'interface GigabitEthernet2',
            'ip address 10.1.3.3 255.255.255.0',
            'interface GigabitEthernet3',
            'ip address 10.2.3.3 255.255.255.0',
            'router ospf 1',
            'network 0.0.0.0 255.255.255.255 area 0'
        ]
    }





username = input("Enter your SSH username: ")
password = getpass("Enter your SSH password: ")

for router,ip in ip_addresses.items():
    router_info = {
    "device_type": "cisco_ios",
    "host": ip,
    "username": username,
    "password": password,
    }
    with ConnectHandler(**router_info) as connection:
        connection.enable()
        print(f"#" * 100)
        print(f"Connecting to Router {router} ")
        print(f"#" * 100,"\n")
        #print(output := connection.send_config_set(routers_config[router]))
        print(connection.send_command("show ip os  ne"))
