import os

class User:
    name:str
    mac_addrs:dict


    def __init__(self, *, name:str, mac_addr_5:str, mac_addr_2_4:str):
        """Constructor for the User object.

        Args:
            name (str): User's name.
            mac_addr_5 (str): User's MAC address for 5GHz WiFi.
            mac_addr_2_4 (str): User's MAC address for 2.4GHz WiFi.

        Returns:
            User: A User object.
        """
        self.name = name
        self.mac_addrs = {
            "5GHz": mac_addr_5,
            "2.4GHz": mac_addr_2_4
        }


    def is_connected(self, interface:str="wlan0") -> (bool, str):
        """Determine whether the user is connected to the given iterface via any of their MAC addresses.

        Args:
            interface (str, optional): Interface to check connectivity to. Defaults to "wlan0".

        Returns:
            bool, str: True if connected, False if not. Also returns string detailing what network the user is conencted to.
        """
        for network, mac in self.mac_addrs.items():
            if mac:
                ip = os.popen(f"arp-scan -l -q -x -N -T {mac} -I {interface} | awk '{{print $1}}'").read().strip().split('\n')
                if len(ip) > 1 or "192.168.0.1" in ip:
                    # Sometimes router at 192.168.0.1 is picked up. Running again seems to fix this.
                    ip = os.popen(f"arp-scan -l -q -x -N -T {mac} -I {interface} | awk '{{print $1}}'").read().strip().split("\n")
                if not ip[0]:
                    continue
                if len(ip) == 1:
                    res = os.popen(f"ping -c1 {ip[0]} | grep 'Destination Host Unreachable'").read()
                    if not res:
                        # No Unreachable message, so host CAN be reached
                        return True, network
        return False, ""
