from os import path
import pandas as pd
import timeit
import sys, argparse, getpass
from netmiko import ConnectHandler
import getpass

# clear contents or delete all created txt files before each run

start = timeit.default_timer()

pwd = getpass.getpass('Enter network password: ')
market = input('Enter tail Market ID (XXXX): ').upper()
head_ip = input('Enter head IP: ')
tail_ip01 = input('Enter tail router 01 IP: ')
tail_ip02 = input('Enter tail router 02 IP: ')

tesla_mrkt = open('tesla_mrkt.txt', 'w', encoding='utf8')
tesla_mrkt.write(f'{head_ip}')
tesla_mrkt.write(f'\n{tail_ip01}')
tesla_mrkt.write(f'\n{tail_ip02}')
tesla_mrkt.close()

with open('tesla_mrkt.txt') as routers:
    for IP in routers:
        Router = {
            'device_type': 'cisco_xr',
            'ip': IP,
            'username': 'tommie.waters',
            'password': f'{pwd}'
        }

        net_connect = ConnectHandler(**Router)

        net_connect.send_command('term length 0')
        sh_hostname = net_connect.send_command('show running-config formal hostname')
        hostname = sh_hostname.split(' ')[5].strip('\n')
        tesla_desc = net_connect.send_command('show interface description | i TESLA')
        explicit_config = net_connect.send_command(f'show run formal explicit | i TESLA | i {market}')
        head_mc = net_connect.send_command('show run formal multicast-routing | i mte')
        tail_mc = net_connect.send_command(f'show run formal multicast-routing | i {head_ip}')
        igmp = net_connect.send_command('show run formal router igmp')
        access_list = net_connect.send_command('show run formal | i access-list P2MP')
        rtr_static = net_connect.send_command('show run formal router static | i Tesla')
        traffic_eng = net_connect.send_command('show run formal mpls traffic-eng | i delay')
        ssm = net_connect.send_command('show run formal ipv4 access-list SSM')
        tesla_info = open('tesla_check.txt', 'a')

        if IP.strip('\n') == head_ip:
            tesla_info.write('=' * 94)
            tesla_info.write(f'\nHEAD MRKT {hostname} {IP}')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(tesla_desc)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(explicit_config)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(head_mc)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(access_list)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(igmp)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
        elif IP.strip('\n') == tail_ip01:
            tesla_info.write(f'TAIL MRKT01 {hostname} {IP}')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(ssm)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(traffic_eng)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(tail_mc)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(access_list)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(rtr_static)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
        else:
            tesla_info.write(f'TAIL MRKT02 {hostname} {IP}')
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(ssm)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(traffic_eng)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(tail_mc)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(access_list)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')
            tesla_info.write(rtr_static)
            tesla_info.write('\n')
            tesla_info.write('=' * 94)
            tesla_info.write('\n')

        tesla_info.close()

    stop = timeit.default_timer()
    total_time = stop - start
    print("\nExecution Time " + f'{total_time}' + " seconds.\n")

net_connect.disconnect()