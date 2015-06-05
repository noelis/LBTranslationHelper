#!/usr/bin/python

import json
import requests
import logging
import time
from requests.auth import HTTPBasicAuth

# change these when you run the script!
email = "email@rd.io" # Use the Rdio emial address associated with your Desk account
password = "password" # Use your Desk account password

date = "2000-02" # Change date
file_name = "our_file" # Change filename
topic = "27647" # Change topic

response = requests.get('https://rdio.desk.com/api/v2/topics/%s/articles' % topic, auth=HTTPBasicAuth(email, password))
data = json.loads(response.content)

print "# of entries is: %s" % (data['total_entries'])
embedded = data['_embedded']
entries = embedded['entries']

f = open('%s.txt' % file_name, 'w')

expored = 0
f.write("[NOTE: for topic %s, all articles updated after %s]\n\n" % (topic, date))
for entry in entries:
  if entry['updated_at'] > date and entry['in_support_center']:
    expored = expored + 1
    f.write(("%s\n" % entry['id']).encode('utf-8'))
    f.write(("%s\n" % entry['subject']).encode('utf-8'))
    f.write(("%s\n" % entry['body']).encode('utf-8'))
    f.write("==================================\n")

    # print "subject: %s \t update: %s" % (x['subject'], x['updated_at'])


print "yoooooo omg1!! we shut pooped out %s in %s" % (expored, file_name)