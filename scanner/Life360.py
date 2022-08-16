import requests
import json

class Life360:
    
    BASE_URL = "https://api.life360.com/v3/"
    TOKEN_URL = "oauth2/token.json"
    CIRCLES_URL = "circles.json"
    CIRCLE_URL = "circles/"

    def __init__(self, authorization_token=None, email=None, password=None):
        self.authorization_token = authorization_token
        self.email = email
        self.password = password

    def make_request(self, url, params=None, method='GET', authheader=None):
        headers = {'Accept': 'application/json'}
        if authheader:
            headers.update({'Authorization': authheader, 'cache-control': "no-cache",})
        
        if method == 'GET':
            r = requests.get(url, headers=headers)
        elif method == 'POST':
            r = requests.post(url, data=params, headers=headers)

        return r.json()

    def authenticate(self):
        

        url = self.BASE_URL + self.TOKEN_URL
        params = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
        }

        r = self.make_request(url=url, params=params, method='POST', authheader="Basic " + self.authorization_token)
        try:
            self.access_token = r['access_token']
            return True
        except:
            return False

    def get_circles(self):
        url = self.BASE_URL + self.CIRCLES_URL
        authheader = "bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r['circles']

    def get_circle(self, circle_id):
        url = self.BASE_URL + self.CIRCLE_URL + circle_id
        authheader = "bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r
