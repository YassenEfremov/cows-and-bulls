import os
import re
import platform


def get_lan_ips():

    # Check operating system

    op_sys = platform.system()

    # Find IP's of all machines on local network

    devices = []

    if op_sys == "Linux":
        for device in os.popen("arp -a"):
            IP_RAW = re.split("\s", device)[1]
            IP = re.sub("[()]", "", IP_RAW)
            devices.append(IP)
    elif op_sys == "Windows":
        for device in os.popen("arp -a"):
            try:
                IP_RAW = re.split("\s", device)[2]
                devices.append(IP_RAW)
                print(IP_RAW)
            except IndexError:
                pass

    return devices