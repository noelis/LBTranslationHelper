#!/usr/bin/python

import json
import requests
import logging
import time
from requests.auth import HTTPBasicAuth


# change these when you run the script!
email = "email@rd.io" # Use the Rdio emial address associated with your Desk account
password = "password" # Use your Desk account password

# REMENBER!! : the zipped files need to live next to the script (same directory)
zip_dir = "lionstuff"
file_name = "Support Translations.txt"

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


# article id    0
# name           1
# white line     2 - ....  ?? N
# stuffffffff for body
# ____________________________
def update_translation(desk_lang, chunk):
  id = chunk[0].strip()
  subject = chunk[1].strip()
  payload = {
    "locale": desk_lang,
    "subject": subject,
    "body": "\n".join(chunk[2:])
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
    if line.startswith("_____"):
      update_translation(desk_lang, chunk)
      chunk = []
    else:
      chunk.append(line)
  update_translation(desk_lang, chunk)