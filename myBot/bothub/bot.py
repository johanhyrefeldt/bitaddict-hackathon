# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel

#%%

import sys
import time
import random
import string
import hashlib
import http.client
import json
from datetime import datetime
import requests

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
    
    return response_json

def hitta_api(plats='goteborg'):
    namsdag = dag_api()[0]

    # Get url from first argument
    url = '/publicsearch/v1/persons?what={}&where={}&range.from=1&range.to=50'.format(namnsdag,plats)

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
    #print("resp.status\n{}\nresp.reason{}".format(resp.status, resp.reason))
    json_response = json.loads(resp.read())
    #print(json.dumps(json_response, indent=4, separators=(',', ': ')))

    #%%
    for el in json_response['result']['persons']['person']:
        name = str(el['displayName'])
        first_name = name.split(" ")[0]
        if first_name.lower() == 'nils':
            message = "Här är dagens namnsdagsbarn :) \n"
            try:
                phone = el['phone'][0]
                phone_number = phone['callTo']
                message = message + "Namn: {} telefonnummer {}\n".format(el['displayName'], phone_number)
            except KeyError:
                message = message + "Namn: {} Ledsen! Inget telefonnummer\n".format(el['displayName'])

    return message

def get_namedate():
    hitta_api()
    str = "Idag har %s namnsdag! \n Gratta hen med nummer: %s" % ("Anders", "073 917 48 46")
    return str

class Bot(BaseBot):
    """Represent a Bot logic which interacts with a user.

    BaseBot superclass have methods belows:

    * Send message
      * self.send_message(message, chat_id=None, channel=None)
    * Data Storage
      * self.set_project_data(data)
      * self.get_project_data()
      * self.set_user_data(data, user_id=None, channel=None)
      * self.get_user_data(user_id=None, channel=None)
    * Channel Handler
      from bothub_client.decorators import channel
      @channel('<channel_name>')
      def channel_handler(self, event, context):
        # Handle a specific channel message
    * Command Handler
      from bothub_client.decorators import command
      @command('<command_name>')
      def command_handler(self, event, context, args):
          # Handle a command('/<command_name>')
    * Intent Handler
      from bothub_client.decorators import intent
      @intent('<intent_id>')
      def intent_result_handler(self, event, context, answers):
          # Handle a intent result
          # answers is a dict and contains intent's input data
            {
              "<intent slot id>" : <entered slot value>
              ...
            }
    """
    @channel()
    def default_handler(self, event, context):
        """Handle a message received

        event is a dict and contains trigger info.

        {
           "trigger": "webhook",
           "channel": "<name>",
           "sender": {
              "id": "<chat_id>",
              "name": "<nickname>"
           },
           "content": "<message content>",
           "raw_data": <unmodified data itself webhook received>
        }
        """
        msg = hitta_api(event["content"])
        self.send_message(msg)

    
