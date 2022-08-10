import os

CONFIG = {
    "MEROSS_EMAIL": os.environ.get('MEROSS_EMAIL'),
    "MEROSS_PASSWORD": os.environ.get('MEROSS_PASSWORD'),
    "MAC_ADDR_FILE": "mac_addrs.csv",
    "INTERFACE": "wlan0"
}
