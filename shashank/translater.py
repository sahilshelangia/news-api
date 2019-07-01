import os
import re
import time
import logging
import MySQLdb
import requests
import warnings
from google.cloud import translate
logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
						format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')
						
logging.info('Info: {}'.format("translater Script Running."))

try:
		translate_client = translate.Client.from_service_account_json('updraft-data-API-key.txt')

		warnings.filterwarnings('ignore', category=MySQLdb.Warning)

		#logging module used for log file creation
		logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
						format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')

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
			logging.info('Info: {}'.format("translator Script Closed."))
			exit("error, see logs")


		#load text files that contains ids of already translated articles
		try:
				ids_file = open('translated_articles_ids.txt','r')
				ids = ids_file.readlines()
				ids = [id.rstrip() for id in ids]
				ids_file.close()
				logging.info('Info: {}'.format("translated articles ids extracted."))
				
		except Exception as error:
				logging.error('Error: {}'.format(error))
				logging.info('Info: {}'.format("translator Script Closed."))
				exit("error,see logs")

		#fetch all english articles
		cursor.execute('use main_database')
		cursor.execute('select * from english_database')
		entries = cursor.fetchall()		

		# ### Language Codes: 
		# Telugu : 'te' 
		# Tamil : 'ta' 
		# Kannada : 'kn' 
		# Bengali : 'bn' 
		# Hindi : 'hi' 

		languages = {'hindi':'hi','tamil':'ta','kannada':'kn','bengali':'bn','telugu':'te'}
		print(ids)
		def new_id(id):
			if id in ids:
				return False
			else:
				return True
		i=0
		for entry in entries[0:6]:
					ide=entry[0]
					title=entry[1]
					link=entry[2]
					source=entry[3]
					summary=entry[4]
					content=entry[5]
					published_date=entry[6]
					if new_id(ide):
							for language,code in languages.items():
								flag=0
								translation = translate_client.translate([title,summary,content],source_language='en',target_language=code)
								string = language + '_database'
								translated_title = translation[0]['translatedText']
								translated_summary = translation[1]['translatedText']
								translated_content = translation[2]['translatedText']
								try:
										cursor.execute('use main_database')
										query_string = 'insert ' + string + ' values (%s,%s,%s,%s,%s,%s,%s)'
										cursor.execute(query_string,(ide,translated_title,link,source,translated_summary,translated_content,published_date))
										print("entry ",i," committed for ",language," language\n")
										
								except Exception as e:
										logging.info('Warn: Article cannot be translated with id = {}, error={}'.format(ide,error))
										flag=1
										break
								
							if (flag == 1):
								continue
							with open('translated_articles_ids.txt','a') as f:
								f.write('{}\n'.format(ide))
							i=i+1
							conn.commit()	
							logging.info('Info: Article successfully translated with id : {}'.format(ide))
		
except Exception as error:
	logging.info('Critical: {}'.format(error))
	print("error, see logs")
		
logging.info('Info: {}'.format("translator Script Closed."))
			
		
		
