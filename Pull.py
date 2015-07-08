#!/usr/bin/env python

import json
import requests
import logging
import time
from requests.auth import HTTPBasicAuth

# change these when you run the script!
#email = "email@rd.io"
#password = "Desk Password"
email = raw_input('Enter your Desk email: ')
password = raw_input('Enter your password: ')

#date = "2000-02"
#file_name = "our_file"
#topic = "27647"
date = raw_input('Pull articles starting from what date? (Please write in this format: YYYY-MM)')
file_name = raw_input(' Enter a file name for these translations:')
topic = raw_input('What is the article topic id number? You can find this in Admin > Content > Topic (like Getting Started) , the ID is located in the URL. ')




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


print "yoooooo omg!! we shut pooped out %s in %s" % (expored, file_name)