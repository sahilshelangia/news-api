import os
import re
import csv
import time
import logging
import hashlib
import MySQLdb
import justext
import requests
import warnings
import feedparser
import urllib.parse
import pandas as pd
import urllib.request
from goose3 import Goose
from boilerpipe.extract import Extractor

warnings.filterwarnings('ignore', category=MySQLdb.Warning)

#logging module used for log file creation
logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
				format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')


logging.info('Info: {}'.format("Categorizer Script Running."))
#load main_database csv to store articles
try:
	conn=MySQLdb.connect(host='localhost',user='root',passwd='')
	conn.set_character_set('utf8')
	cursor = conn.cursor()
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	logging.info('info:Database loaded successfully.')
    
except Exception as error:
	logging.critical('Error: {}'.format(error))
	logging.info('Info: {}'.format("Categorizer Script Closed."))
	exit("error, see logs")


#load text files that contains links of already extracted articles
try:
		ids_file = open('already_categorized_articles_ids.txt','r')
		ids = ids_file.readlines()
		ids = [id.rstrip() for id in ids]
		ids_file.close()
		logging.info('Info: {}'.format("Already viewed ids extracted."))
		
except Exception as error:
		logging.error('Error: {}'.format(error))
		logging.info('Info: {}'.format("Categorizer Script Closed."))
		exit("error,see logs")

cursor.execute('use main_database')
cursor.execute('select * from english_database')
entries = cursor.fetchall()


#check if an article is already categorized
def new_id(id):
	if id in ids:
		return False
	else:
		return True

i=0
for entry in entries:
		id=entry[0]
		if new_id(id):
			title=entry[2]
			content=entry[6]
			#below code snippet will categorize articles based on keywords in keywords.txt file
			category_bool=[]
			category_bool=[id]+category_bool
			with open('keywords.txt','r') as file:
					general=1
					for line in file:
						flag=0
						line = line.rstrip()
						keywords = line.split(',')
						for keyword in keywords:
							title=title.lower()
							content=content.lower()
							if keyword in title:
								general=0
								flag=1
							if keyword in content:
								general=0
								flag=1
						category_bool=category_bool+[flag]
					varlist=category_bool+[general]
					var_string = ', '.join('?' * len(varlist))
					cursor.execute('use main_database')
					query_string = 'INSERT INTO categorized_articles_ids VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
					%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
					cursor.execute(query_string, varlist)
					with open('already_categorized_articles_ids.txt','a') as f:
								f.write('{}\n'.format(id))
			i=i+1
			conn.commit()
			print("entry with title: " ,title," committed\n\n")



logging.info('Info: {}'.format("Categorizer Script Closed."))
