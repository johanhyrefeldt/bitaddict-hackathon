#!/usr/bin/env python
import sys
import time
import random
import string
import hashlib
import http.client
import json

# Get url from first argument
url = '/publicsearch/v1/address/celsiusgatan10stockholm'

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
print("{}, {}".format(resp.status, resp.reason))
json_response = json.loads(resp.read())
print(json.dumps(json_response, indent=4, separators=(',', ': ')))