from Life360 import Life360
import datetime

AUTHORIZATION_TOKEN = "OWE5MDc4YTcxMjRkNjFkYjc1NGNjNzI4NjY2OTRkNWYwNDk2ODY2NDA6NjA2Nzk3MzkwODViYmMxZWY2ZjQyZjlmMDc3YjIwNTA=="  # TODO: Put this in config file
EMAIL = ""  # TODO: Put this in config file
PASSWORD = ""  # TODO: Put this in config file

def life360_login(func):
    def wrapper(authorization_token:str, email:str, password:str, *args, **kwargs):
        api = Life360(authorization_token=authorization_token, email=email, password=password)
        if api.authenticate():
            func(*args, **kwargs, api=api)
        else:
            print("Error authenticating")  # TODO: Deal with this better
    return wrapper

@life360_login(authorization_token=AUTHORIZATION_TOKEN, email=EMAIL, password=PASSWORD)
def get_circle_by_name(circle_name:str, api=None) -> :
    circles = api.get_circles()
    for circle in circles:
        if circle['name'] == circle_name:
            return api.get_circle(circle['id'])
    return {}

def find_users_at_location(circle:dict, location:str) -> list:
    for member in circle['members']:
        

if __name__ == "__main__":

    # basic authorization hash (base64 if you want to decode it and see the sekrets)
    # this is a googleable or sniffable value. i imagine life360 changes this sometimes. 
    #instantiate the API
    api = life360(authorization_token=authorization_token, email=email, password=password)
    if api.authenticate():

        #Grab some circles returns json
        circles =  api.get_circles()
        
        #grab id
        print(circles)
        id = circles[0]['id']

        #Let's get your circle!
        circle = api.get_circle(id)

        #Let's display some goodies

        print ("Circle name:", circle['name'])
        print ("Members (" + circle['memberCount'] + "):")
        for m in circle['members']:

            print("\tName:", m['firstName'],m['lastName'])
            try:
                print("\tLocation:" , m['location']['name'])
                print("\tLatLng:" , m['location']['latitude'] +", "+ m['location']['longitude'])
                print("\tHas been at " +m['location']['name'] +" since " + prettydate(datetime.datetime.fromtimestamp(int(m['location']['since']))))
            except:
                print("Location services off")
            print("\tBattery level:" , m['location']['battery'] +"%")
            print("\t")
    else:
        print ("Error authenticating")
