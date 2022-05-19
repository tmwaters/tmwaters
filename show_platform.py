from netmiko import ConnectHandler
import timeit
import getpass

start = timeit.default_timer()
user = input('Enter network username: ')
pwd = getpass.getpass('Enter network password: ')

with open('mrkt_routers_la.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_xr',
            'ip': IP,
            'username': f'{user}',
            'password': f'{pwd}'
        }

        net_connect = ConnectHandler(**Router)
        net_connect.send_command('term length 0')
        sh_hostname = net_connect.send_command('show running-config formal hostname')
        hostname = sh_hostname.split(' ')[5].strip('\n')
        sh_platform = net_connect.send_command('admin show platform')
        router_hardware = open('cdp_la.txt', 'a', encoding='utf-8')
        router_hardware.write(f'Router {hostname} {IP}')
        router_hardware.write('\n')
        router_hardware.write('-' * 77)
        router_hardware.write('\n')
        router_hardware.write(sh_platform)
        router_hardware.write('\n')
        router_hardware.write('-' * 77)
        router_hardware.write('\n')

    stop = timeit.default_timer()
    total_time = stop - start
    print("\nExecution Time " + f'{total_time}' + " seconds.\n")

# close the connection
net_connect.disconnect()