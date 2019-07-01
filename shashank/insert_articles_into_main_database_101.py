import os
import re
import csv
import time
import json
import logging
import hashlib
import MySQLdb
import justext
import requests
import warnings
import feedparser
import urllib.parse
import pandas as pd
from time import mktime
import urllib.request
from datetime import datetime
from goose3 import Goose
from boilerpipe.extract import Extractor

uri = 'http://www.agriiprince.com/test/php_test.php'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

warnings.filterwarnings('ignore', category=MySQLdb.Warning)

#logging module used for log file creation
logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
				format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')


logging.info('Info: {}'.format("Insert_article_into_database Script Running."))

	
#load rss sources from which articles are be extracted	
try:
		rss_file = open('rss_sources.txt','r')
		rss_list = rss_file.readlines()
		rss_list = [rss.rstrip() for rss in rss_list]
		rss_file.close()
		logging.info('Info: {}'.format("rss sources extracted."))
		
except Exception as error:
		logging.error('Error: {}'.format(error))
		logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
		exit("error,see logs")
	
	
	
#load text files that contains ids of already extracted articles
try:
		ids_file = open('viewed_articles_ids.txt','r')
		ids = ids_file.readlines()
		ids = [id.rstrip() for id in ids]
		ids_file.close()
		logging.info('Info: {}'.format("Already viewed ids extracted."))
		
except Exception as error:
		logging.error('Error: {}'.format(error))
		logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
		exit("error,see logs")



#check if internet connection present
def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
					_ = requests.get(url, timeout=timeout)
					logging.info('Info: {}'.format("Internet Connection Established"))
    except Exception as error:
				 logging.error('Error: {}'.format("Failed to create internet connection."))
				 logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
				 exit("error, see logs")

check_internet()

#function to check if an article is already in database
def new_id(id):
	if id in ids:
		return False
	else:
		return True

print("Fetching...\n")
#extract all articles from a rss source and push into database(excel file)
def extract_rss_articles(rss):
			
			new_entries_inserted=0
			try:
				#rss parser
				rss_feed = feedparser.parse(rss)
				
			except:
				logging.warn('Warn: Parsing failed for rss source={}'.format(rss))
				return 0
				
			for entry in rss_feed['entries']:
					
					#title extracted
					if 'title' in entry.keys():
						title=entry.title
					else:
						continue
					
					#link extracted
					if 'link' in entry.keys():
						link = entry.link
						source=link.split("//")[-1].split("/")[0]
					else:
					    continue
					id = hashlib.md5((title+link).encode("utf-8")).hexdigest()
					
					if new_id(id):
							
							#date of publish of article extracted
							if 'published_parsed' in entry.keys():
								published_date = entry.published_parsed
								published_date = datetime.fromtimestamp(mktime(published_date)).isoformat()
								published_date = published_date.split("T")[0]
							else:
								published_date = "0000-00-00"
							#print(published_date)
							
							#summary of article extracted
							if 'summary' in entry.keys():
								summary=entry['summary']
							else:
								summary=""
							TAG_RE = re.compile(r'<[^>]+>')
							summary = TAG_RE.sub('', summary)
							
							#extract full content of article
							content=""
							if rss!="https://services.india.gov.in/feed/rss?cat_id=12&ln=en":
								if rss=="http://goidirectory.nic.in/rss/minstry_rss.php?categ_id=1":
									try:
										response = requests.get(link)
										paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
										for paragraph in paragraphs:
										 if not paragraph.is_boilerplate:
													content = content + paragraph.text	
									except:
										content = ""
								else:
									try:
										extractor = Extractor(extractor='ArticleSentencesExtractor', url=link)
										content = extractor.getText()
									except:
										content = ""
									
							else:
								content=summary
							
							if content=="" or content=="unknown":
								continue	
							
							#insert article into database
							try:
								'''
								cursor.execute('use main_database')
								cursor.execute('insert english_database values (%s,%s,%s,%s,%s,%s,%s)',(id,published_date,title,link,source,summary,content))
								logging.info('Info: New Article pushed into database from {}'.format(source))
								conn.commit()	
								print("Article Fetched")
								'''
								
								id=str(id)
								published_date=str(published_date)
								title=str(title)
								link=str(link)
								source=str(source)
								summary=str(summary)
								content=str(content)
								k=0
								k=k+1
								
								title = title.replace("'","")
								summary=summary.replace("'","")
								content=content.replace("'","")
								
								query = """INSERT INTO english_database VALUES('{id}','{date}','{title}','{link}','{source}','{summary}','{content}');""".format(id = id,date = published_date,title = title, link = link,source = source, summary = summary, content = content)
										
								print("Article Fetched1")
								#query = "INSERT INTO english_database VALUES("
								#insert_tuple = id+','+published_date+','+title+','+link+','+source+','+summary+','+content+");"
								#query=query+insert_tuple
								#print(query)
								print("Article Fetched2")

								list=[query]
								formDict = {}
								formDict['values'] = json.dumps(list)
								formDict['rofl'] = 'Xz6mUMy4pFgMamyBu8hkWuq'
								session = requests.Session()
								resp = session.post(uri,headers=headers,data=formDict)
								session.close()								
								print("Article pushed in database")
								
							except Exception as error:
								print(error)
								logging.info('Warn: Article cannot be pushed from source {}, error={}'.format(source,error))
								continue
							
							#insert the link of this article into viewed_links.txt, since it has been viewed
							with open('viewed_articles_ids.txt','a') as f:
								f.write('{}\n'.format(id))
							new_entries_inserted = new_entries_inserted+1			
			print("rss source processed")
			#return count of new entries inserted into database
			return new_entries_inserted

#new rss source must be appended in this list


#total new entries inserted into database
total_entries = 0

#iterate over all rss sources 
for rss in rss_list:
	total_entries = total_entries + extract_rss_articles(rss)

#print total new entries inserted
print(total_entries," new entries are inserted into database.")					


logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))















