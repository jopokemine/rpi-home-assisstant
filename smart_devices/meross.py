import asyncio
import os
from random import randint
import yaml
from config import CONFIG

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.enums import OnlineStatus

# with open("/config.yml", 'r') as yml:
#     cfg = yaml.safe_load(yml)

# EMAIL = cfg["meross"]["email"]
# PASSWORD = cfg["meross"]["passwd"]

EMAIL = CONFIG['MEROSS_EMAIL']
PASSWORD = CONFIG['MEROSS_PASSWORD']

# EMAIL = os.environ.get('MEROSS_EMAIL')
# PASSWORD = os.environ.get('MEROSS_PASSWORD')


def async_func(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()
    return wrapper


def meross_login(func):
    async def wrapper(*args, **kwargs):
        # Setup the HTTP client API from user-password
        http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

        # Setup and start the device manager
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        await manager.async_device_discovery()

        # Run the function
        await func(*args, **kwargs, manager=manager)

        # Close the manager and logout from http_api
        manager.close()
        await http_api_client.async_logout()
    return wrapper


@async_func
@meross_login
async def turn_off_lights(user=None, manager=None):
    lights = manager.find_devices(device_type="msl120d",
                                  online_status=OnlineStatus.ONLINE)
    
    if len(lights) < 1:
        print("No online msl120d smart bulbs found...")  # TODO: figure out how to deal with this
    else:
        for light in lights:
            await light.async_update()
            if (user is None or user in light.name.lower()) and light.is_on():
                await light.async_turn_off(channel=0)


@async_func
@meross_login
async def main(manager=None):
    plugs = manager.find_devices(
        device_type="msl120d", online_status=OnlineStatus.ONLINE)

    if len(plugs) < 1:
        print("No online msl120d smart bulbs found...")
    else:
        # Let's play with RGB colors. Note that not all light devices will support
        # rgb capabilities. For this reason, we first need to check for rgb before issuing
        # color commands.
        dev = plugs[0]

        # Update device status: this is needed only the very first time we play with this device (or if the
        #  connection goes down)
        await dev.async_update()
        print(f"Light is on: {dev.is_on()}")
        # if not dev.get_supports_rgb():
        #     print("Unfortunately, this device does not support RGB...")
        # else:
        #     # Check the current RGB color
        #     current_color = dev.get_rgb_color()
        #     print(
        #         f"Currently, device {dev.name} is set to color (RGB) = {current_color}")
            
        #     print(f"Turning on {dev.name}")
        #     await dev.async_turn_on(channel=0)
        #     print("Waiting 5 seconds to turn back off")
        #     await asyncio.sleep(5)
        #     print(f"Turning off {dev.name}")
        #     await dev.async_turn_off(channel=0)
            # Randomly chose a new color
            # rgb = randint(0, 255), randint(0, 255), randint(0, 255)
            # print(f"Chosen random color (R,G,B): {rgb}")
            # await dev.async_set_light_color(rgb=rgb)
            # print("Color changed!")

# if __name__ == '__main__':
#     main()
    # turn_off_all_lights()
# turn_off_user_lights("josh")
