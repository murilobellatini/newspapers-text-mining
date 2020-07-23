"""
Script to test if API run succeeded
"""
import json
import requests

url = 'http://localhost:8000/api/'
data = {
    'item_id': 1,
    'text': 'Trump Steps Up His Assault on Biden With Scattershot Attacks, Many False'
}
j_data = json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

if __name__ == "__main__":
    r = requests.post(url, data=j_data, headers=headers)
    print(r, r.text)