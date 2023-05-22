import requests
from env import *

json = {
            "prompt" :  "huh",
            }
response = requests.post(url=f"{Koblod_LINK}/api/v1/story/end", json = json)