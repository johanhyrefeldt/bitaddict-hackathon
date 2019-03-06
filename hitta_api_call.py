#%%
#!/usr/bin/env python
import sys
import time
import random
import string
import hashlib
import http.client
import json
from datetime import datetime
import requests

# Get url from first argument
url = '/publicsearch/v1/persons?what=Nils&range.from=1&range.to=50'

# Authentication parameters
caller_id = "Lag1"
time = str(int(time.time()))
key =  "cq9MxlplYqbiAtiPZctvhNqlWaHRsaEUgSZj57uk"
random = "".join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(16))

# Create the hashed string
string_to_hash = caller_id + time + key + random
hashed_string = hashlib.sha1(string_to_hash.encode('utf-8')).hexdigest()

# The http headers
headers = {
   "X-Hitta-CallerId": caller_id,
   "X-Hitta-Time": time,
   "X-Hitta-Random": random,
   "X-Hitta-Hash": hashed_string
}

# Make the call
conn = http.client.HTTPSConnection("api.hitta.se")
conn.request("GET", url, "", headers)
resp = conn.getresponse()

# Print response
print("resp.status\n{}\nresp.reason{}".format(resp.status, resp.reason))
json_response = json.loads(resp.read())
print(json.dumps(json_response, indent=4, separators=(',', ': ')))
print("#########")

def dag_api():
    datet = datetime.now() 
    day = str(datet.day)
    month = str(datet.month)
    year = str(datet.year)

    url_day = ('http://api.dryg.net/dagar/v2.1/'+year+'/'+month+'/'+day)

    print('date url:',url_day)
    
    resp = requests.get(url_day)
    #print(resp.json())
    response_json = resp.json()['dagar'][0]['namnsdag']
    print(response_json)

#%%
for el in json_response['result']['persons']['person']:
    name = str(el['displayName'])
    first_name = name.split(" ")[0]
    if first_name.lower() == 'nils':
        try:
            phone = el['phone'][0]
            phone_number = phone['callTo']
            print("Name: {}\t\t phone number {}".format(el['displayName'], phone_number))
        except KeyError:
            print("Name: {}\t\t Sorry! No phone number".format(el['displayName']))
        # print(json.dumps(el, indent=2, separators=(',', ': ')))
