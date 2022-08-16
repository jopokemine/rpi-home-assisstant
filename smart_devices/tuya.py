import tinytuya as tt

# from config import CONFIG


DEVICE_ID:str = "800061668caab5007d98"
IP_ADDRESS:str = "192.168.0.43"
LOCAL_KEY:str = "ef71832117a0792c"

d = tt.BulbDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
d.set_version(3.3)

data = d.status()

print('set_status() result %r' % data)

# Turn On
d.turn_off()
