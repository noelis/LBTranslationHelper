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

# REMENBER!! : the zipped files need to live next to the script (same directory)
#zip_dir = "emily"
#file_name = "HelpArticles-June2015.txt"
zip_dir = raw_input('What is the name of the folder of the unzipped translations? ')
file_name = raw_input('What is the name of the .txt file inside the folder? (Include .txt in the name.)')

language_map = {
  'cs-cz' : 'cs',
  'da-dk' : 'da',
  'de-ch' : 'de_ch',
  'de-de' : 'de',
  'es-xl' : 'es',
  'fi-fi' : 'fi',
  'fr-fr' : 'fr',
  'hu-hu' : 'hu',
  'id-id' : 'id',
  'it-it' : 'it',
  'nb-no' : 'no',
  'nl-nl' : 'nl',
  'pl-pl' : 'pl',
  'pt-br' : 'pt_br',
  'pt-pt' : 'pt',
  'sv-se' : 'sv',
  'th-th' : 'th',
  'zh-hk' : 'zh_tw',
  # DO THE OTHER ONES
}


# acrticle id    0
# name           1
# white line     2 - ....  ?? N
# stuffffffff for body
# ==============================
def update_translation(desk_lang, chunk):
  id = chunk[0].strip()
  subject = chunk[1].strip()
  payload = {
    "locale": desk_lang,
    "subject": subject,
    "body": "\n".join(chunk[2:]),
    "publish_at": "2015-07-04T22:28:53Z"
  }

  print " > processing [%s] %s" % (id, subject)
  response = requests.post('https://rdio.desk.com/api/v2/articles/%s/translations' % id, 
    data=json.dumps(payload),
    auth=HTTPBasicAuth(email, password))

  if response.status_code == 422:
    print " >>> updating"
    response = requests.patch('https://rdio.desk.com/api/v2/articles/%s/translations/%s' % (id, desk_lang), 
      data=json.dumps(payload),
      auth=HTTPBasicAuth(email, password))
  else:
    print " >>> created"

  if response.status_code != 200:
    print " >>> %s" % response

for lion_lang in language_map:
  desk_lang = language_map[lion_lang]
  print "Handling %s -> %s " % (lion_lang, desk_lang)
  f = open('%s/%s/%s' % (zip_dir, lion_lang, file_name))
  chunk = []
  for line in f:
    if line.startswith("========="):
      update_translation(desk_lang, chunk)
      chunk = []
    else:
      chunk.append(line)
  update_translation(desk_lang, chunk)