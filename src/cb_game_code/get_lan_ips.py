import os
import re
import platform


def get_lan_ips():
    """
    Executes "arp -a" in terminal and gets the LAN IPs (uses different methods based on the OS)
    """

    # Check operating system

    op_sys = platform.system()

    # Place all the LAN IPs in a list

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
            except IndexError:
                pass

    return devices