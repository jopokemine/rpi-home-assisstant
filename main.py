import asyncio
from scanner import get_users_connection_status
from smart_devices import turn_off_lights
from config import CONFIG
import os
from datetime import datetime

if __name__ == "__main__":
    users_conn_status = get_users_connection_status(CONFIG["MAC_ADDR_FILE"], CONFIG["INTERFACE"])
    users_disconnected = []
    now = datetime.now()
    curr_time = now.strftime("%H:%M")
    with open("users_conn_status.txt", 'w') as f:
        for user in users_conn_status:
            if user[1]:
                print(f"{user[0]} is connected to the {user[2]} network at {curr_time}")
                f.write(f"{user[0]} is connected to the {user[2]} network at {curr_time}\n")
            else:
                print(f"{user[0]} is disconnected at {curr_time}")
                f.write(f"{user[0]} is disconnected at {curr_time}\n")
                users_disconnected.append(user[0])

    # if [user[0] for user in users_conn_status] == users_disconnected:
    #     # All devices disconnected.
    #     turn_off_lights()
    # else:
    #     for user in users_disconnected:
    #         if user != "mum":
    #             # TODO: Finish this - tuya?
    #             turn_off_lights(user)

        # if not user[1] and user[0] != "mum":
        #     print(f"{user[0]} is not connected, turning off devices...")
        #     turn_off_lights(user[0])
