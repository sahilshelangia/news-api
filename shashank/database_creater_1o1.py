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
from boilerpipe.extract import Extractor
import logging
import MySQLdb
import warnings


logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
				format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')

uri = 'http://www.agriiprince.com/test/php_test.php'
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

list = [
'SET NAMES utf8;',
'SET CHARACTER SET utf8;',
'SET character_set_connection=utf8;',
'use dbs27033',
'Create table english_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table hindi_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table tamil_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table bengali_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table telugu_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table kannada_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)',
'Create table categorized_articles_ids(id char(64) PRIMARY KEY,Tips_for_Farmer int,Technologies_of_Ne_India int,Best_Practices_Farming int,Technology int,Seeds int,Agriculture_News int,Cold_Chain int,Sustainable_Agriculture int, Precision_Farming_Tools_Technology int,Weather_Information int,Technologies int,Entrepreneurship_Programme int,Pest_Management int,herbicides int,Nutrient_Management int, Crop_Selection int,Established_Standards_and_Practices int,Natural_Farming_News int,Natural_Resins int,fertilizers int,Crop_management int,crops int,Organic_farming int,Pricing_Equipments int,Agriculture_seeds int,Traits_and_Technology int,Production_practices int,Organic int,Inorganic_Inputs int,Crop_Seeds int, Farm_Machinery int,Weed_management_products int,Advance_Technologies int,Bio_Inputs int,Pest_Control int,Weed_Management int,Farm_Management int,Farm_Services int,nutrients int, General_News int)',
'ALTER TABLE `english_database` CONVERT TO CHARACTER SET `utf8`',
'ALTER TABLE `hindi_database` CONVERT TO CHARACTER SET `utf8`',
'ALTER TABLE `tamil_database` CONVERT TO CHARACTER SET `utf8`',
'ALTER TABLE `bengali_database` CONVERT TO CHARACTER SET `utf8`',
'ALTER TABLE `telugu_database` CONVERT TO CHARACTER SET `utf8`',
'ALTER TABLE `kannada_database` CONVERT TO CHARACTER SET `utf8`',
]
formDict = {}
formDict['values'] = json.dumps(list)
formDict['rofl'] = 'Xz6mUMy4pFgMamyBu8hkWuq'

print("Empty Database created\n\n")

logging.info('Info: {}'.format("New database created."))

file = open("viewed_articles_ids.txt", "w")  
file.close()
file = open("already_categorized_articles_ids.txt", "w")  
file.close()
file = open("translated_articles_ids.txt", "w")  
file.close()


session = requests.Session()
resp = session.post(uri,headers=headers,data=formDict)
session.close()
print("Done")
