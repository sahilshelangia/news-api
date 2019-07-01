import logging
import MySQLdb
import warnings

logging.basicConfig(filename='log_file.log', level=logging.DEBUG,
				format='Time: %(asctime)s, Logged At Line: %(lineno)d, %(message)s')

conn=MySQLdb.connect(host='localhost',user='root',passwd='')
conn.set_character_set('utf8')
cursor = conn.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
	
	
conn=MySQLdb.connect(host='localhost',user='root',passwd='')
conn.set_character_set('utf8')

try:
	cursor.execute("DROP database main_database")
	logging.info('Info: {}'.format("Existing database deleted."))

except:
	logging.info('Info: {}'.format("No old database found."))

try:
	cursor.execute('Create database main_database')
	cursor.execute('use main_database')
	cursor.execute('Create table english_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table hindi_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table kannada_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table tamil_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table bengali_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table telugu_database(id   CHAR(64) PRIMARY KEY,article_published_date date, article_title text, article_link text, article_source text, article_summary text, article_content text)')
	cursor.execute('Create table categorized_articles_ids(id char(64) PRIMARY KEY,Tips_for_Farmer int,Technologies_of_Ne_India int,Best_Practices_Farming int,Technology int,Seeds int,Agriculture_News int,Cold_Chain int,Sustainable_Agriculture int, Precision_Farming_Tools_Technology int,Weather_Information int,Technologies int,Entrepreneurship_Programme int,Pest_Management int,herbicides int,Nutrient_Management int, Crop_Selection int,Established_Standards_and_Practices int,Natural_Farming_News int,Natural_Resins int,fertilizers int,Crop_management int,crops int,Organic_farming int,Pricing_Equipments int,Agriculture_seeds int,Traits_and_Technology int,Production_practices int,Organic int,Inorganic_Inputs int,Crop_Seeds int, Farm_Machinery int,Weed_management_products int,Advance_Technologies int,Bio_Inputs int,Pest_Control int,Weed_Management int,Farm_Management int,Farm_Services int,nutrients int, General_News int)')
	cursor.execute('ALTER TABLE `hindi_database` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `categorized_articles_ids` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `bengali_database` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `kannada_database` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `telugu_database` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `tamil_database` CONVERT TO CHARACTER SET `utf8`')
	cursor.execute('ALTER TABLE `english_database` CONVERT TO CHARACTER SET `utf8`')
	print("Empty Database created\n\n")
	logging.info('Info: {}'.format("New database created."))
	file = open("viewed_articles_ids.txt", "w")  
	file.close()
	file = open("already_categorized_articles_ids.txt", "w")  
	file.close()
	file = open("translated_articles_ids.txt", "w")  
	file.close()

except Exception as error:
	logging.info('Info: {}'.format(error))
	print("error, see logs")


