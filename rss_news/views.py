from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as soup
import datetime as dt
import json
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
from datetime import datetime,date,time
# from boilerpipe.extract import Extractor
import logging
import MySQLdb
import warnings
from django.shortcuts import get_object_or_404
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from .models import Article,ArticleTitle



def base(request):
	return render(request,'base.html')

# Create your views here.
def index(request):
	return render(request,'rss_news/index.html')

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
					_ = requests.get(url, timeout=timeout)
					logging.info('Info: {}'.format("Internet Connection Established"))
					print("Internet Connection Established")
    except Exception as error:
				 logging.error('Error: {}'.format("Failed to create internet connection."))
				 logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
				 print("Failed to create internet connection.")
				 exit("error, see logs")


ids=[]
#function to check if an article is already in database
def new_id(id):
	if id in ids:
		return False
	else:
		return True






#extract all articles from a rss source and push into database(excel file)
def extract_rss_articles(rss):
	new_entries_inserted=0
	try:
		#rss parser
		rss_feed = feedparser.parse(rss)		
	except:
		logging.warn('Warn: Parsing failed for rss source={}'.format(rss))
		return 0
		
	auto_incr_id=0;
	for entry in rss_feed['entries']:
			auto_incr_id+=1
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
						tmp=str(published_date[0])+"-"+str(published_date[1])+"-"+str(published_date[2]);
						published_date=tmp
					else:
						published_date = "0000-00-00"
					print(published_date)
					

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
							try:
								response = requests.get(link)
								paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
								for paragraph in paragraphs:
								 if not paragraph.is_boilerplate:
											content = content + paragraph.text	
							except:
								content = ""
						
							
					else:
						content=summary
					
					if content=="" or content=="unknown":
						continue

					#insert article into database
					try:
						print("Result==============")
						try:
							newsArticle=get_object_or_404(Article,id=auto_incr_id)
							if newsArticle:
								newsArticle.published_date=published_date
								newsArticle.title=title
								newsArticle.link=link
								newsArticle.source=source
								newsArticle.summary=summary
								newsArticle.content=content
								newsArticle.save()
						except:
							newsArticle=Article.objects.create(id=auto_incr_id,published_date=published_date,title=title,link=link,source=source,summary=summary,content=content)
							newsArticle.save()

						try:
							newsArticleTitle=get_object_or_404(ArticleTitle,id=auto_incr_id)
							if newsArticleTitle:
								newsArticleTitle.title=title
								newsArticleTitle.summary=summary
								newsArticleTitle.save()
						except:								
							newsArticleTitle=ArticleTitle.objects.create(id=auto_incr_id,title=title,summary=summary)
							newsArticleTitle.save()
						print(id,published_date,title,link,source,summary,content)
						print("Article Fetched")
						'''
						query = """INSERT INTO english_database VALUES('{id}','{date}','{title}','{link}','{source}','{summary}','{content}');""".format(id = id,date = published_date,title = title, link = link,source = source
								,summary = summary, content = content)
						#print(query)
						cursor.execute(query)
						conn.commit()
						'''
					except Exception as error:
						logging.info('Warn: Article cannot be pushed from source {}, error={}'.format(source,error))
						continue
					
					#insert the link of this article into viewed_links.txt, since it has been viewed
					with open('viewed_articles_ids.txt','a') as f:
						f.write('{}\n'.format(id))
					new_entries_inserted = new_entries_inserted+1			
	print("rss source processed")
	#return count of new entries inserted into database
	return new_entries_inserted


def collectNews(request):
	uri = 'http://www.agriiprince.com/test/php_test.php'
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	}

	try:
		path=os.path.join(BASE_DIR,'shashank/rss_sources.txt')
		rss_file = open(path,'r')
		rss_list = rss_file.readlines()
		rss_list = [rss.rstrip() for rss in rss_list]
		rss_file.close()
		logging.info('Info: {}'.format("rss sources extracted."))
		print("=================urls================")
		for add in rss_list:
			print(add)
			
	except Exception as error:
			logging.error('Error: {}'.format(error))
			logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
			exit("error,see logs")


	#load text files that contains ids of already extracted articles
	try:
			ids_file = open('shashank/viewed_articles_ids.txt','r')
			ids = ids_file.readlines()
			ids = [id.rstrip() for id in ids]
			ids_file.close()
			logging.info('Info: {}'.format("Already viewed ids extracted."))
			print("=================ids already generated================")
			for idd in ids:
				print(idd)
			
	except Exception as error:
			logging.error('Error: {}'.format(error))
			logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
			exit("error,see logs")


	check_internet()
	print("Fetching...\n")
	#new rss source must be appended in this list


	#total new entries inserted into database
	total_entries = 0

	#iterate over all rss sources 
	for rss in rss_list:
		total_entries = total_entries + extract_rss_articles(rss)

	#print total new entries inserted
	print(total_entries," new entries are inserted into database.")					


	logging.info('Info: {}'.format("Insert_article_into_database Script Closed."))
	return render(request,'rss_news/scrap.html',{'total_entries':total_entries})

def listScrapedArticle(request):
	articles=Article.objects.all()
	return render(request,'rss_news/list.html',{'articles':articles})
