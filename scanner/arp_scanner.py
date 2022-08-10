import csv
import os
from .User import User


def _get_users_from_file(csvf:str) -> list:
    """Get known mac adresses from specified file. Return
    as a list of tuples.

    Args:
        file (str, optional): Relative path to file containing mac addresses.

    Returns:
        list: List of tuples, containing the mac_address and who the mac address corresponds to.
    """
    users = []
    with open(csvf, 'r') as f:
        for line in csv.DictReader(f):
            users.append(User(**line))
    return users


def get_users_connection_status(user_file:str, interface:str="wlan0") -> list:
    """Gets the conenction status of each user, and returns a list of tuples with the connection status.

    Args:
        user_file (str): File path to file with user details in
        interface (str): Interface to connect to. Defaults to "wlan0".

    Returns:
        list: List of tuples, containing the uesr name and if they are connected.
    """
    users = _get_users_from_file(user_file)
    return [(user.name, *user.is_connected(interface)) for user in users]
