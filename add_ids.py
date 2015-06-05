#!/usr/bin/python

import os
import shutil

INPUT_ROOT = 'lionstuff'
OUTPUT_ROOT = 'bearstuff'
FILE_NAME = 'Support Translations.txt'
ROKU_DELIMITER = '____________________________'
PAYPAL_DELIMITER = '____________________________________'


article_ids = {
	'Free': '1967941',
	'Roku': '1967935',
	'Paypal': '1932490'
}

for subdir in os.listdir(INPUT_ROOT):
	if os.path.exists(os.path.join(OUTPUT_ROOT, subdir)):
		shutil.rmtree(os.path.join(OUTPUT_ROOT, subdir))

	os.mkdir(os.path.join(OUTPUT_ROOT, subdir))
	input_fh = open(os.path.join(INPUT_ROOT, subdir, FILE_NAME))

	output_fh = open(os.path.join(OUTPUT_ROOT, subdir, FILE_NAME), 'w')

	output_fh.write(article_ids['Free'] + '\n')
	for line in input_fh:
		clean_line = line.strip()
		output_fh.write(clean_line + '\n')
		if clean_line == ROKU_DELIMITER:
			output_fh.write(article_ids['Roku'] + '\n')
		elif clean_line == PAYPAL_DELIMITER:
			output_fh.write(article_ids['Paypal'] + '\n')

	input_fh.close()
	output_fh.close()