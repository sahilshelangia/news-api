
# coding: utf-8

# In[10]:


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


# In[11]:


def new_id(id):
    if id in ids:
        return False
    else:
        return True


# In[ ]:


try:
        ids_file = open('translated_articles_ids.txt','r')
        ids = ids_file.readlines()
        print(ids)
        ids = [id.rstrip() for id in ids]
        ids_file.close()
        logging.info('Info: {}'.format("translated articles ids extracted."))

except Exception as error:
        logging.error('Error: {}'.format(error))
        logging.info('Info: {}'.format("translator Script Closed."))
        exit("error,see logs")



k=0
for entry in entries:
    ide=entry[0]
    published_date=entry[1]
    if published_date is None:
        published_date = '0000-00-00'
    print(published_date)
    title=entry[2]
    link=entry[3]
    source=entry[4]
    summary=entry[5]
    content=entry[6]
    
    if new_id(ide):
            flag=0
            for language,code in languages.items():
                
                    #print("TRANSLATION FOR ARTICLE NO.= ",k, "STARTED IN ",language.upper(),"LANGUAGE")
                    translation = translate_client.translate(title,source_language='en',target_language=code)

                    try_number = 1
                    while(1):
                        
                        try:
                            translation = translate_client.translate(title,source_language='en',target_language=code)
                            translated_title = translation['translatedText']
                            print("title for article no. ",k," translated." )
                            break
                        except:
                            try_number = try_number + 1
                            if try_number>10:
                                exit("Error, too much waiting, Translation Server Busy or Internet error.")
                                
                            print("sleeping for 10 seconds due to user limit exceed")
                            time.sleep(10)
                        
                    try_number=1
                    while(1):

                        try:
                            translation = translate_client.translate(summary,source_language='en',target_language=code)
                            translated_summary = translation['translatedText']
                            print("summary for article no. ",k," translated." )
                            break
                        except:
							
                            print("sleeping for 10 seconds due to user limit exceed")
                            try_number=try_number+1
                            if try_number>10:
                                exit("Error, too much waiting, Translation Server Busy or Internet error.")
                            time.sleep(10)
                        


                    
                    #breaking of big content text into parts
                    j=0
                    stop_count=0
                    original_content_parts=[]
                    for i in range(0,len(content)):
                        #print(text[j:i])
                        if i == len(content)-1:
                            original_content_parts.append(content[j:i+1])
                            break
                        if content[i]==".":
                            stop_count=stop_count+1
                            if stop_count%50==0:
                                original_content_parts.append(content[j:i])
                                j=i+1
                                
                                
                    print("Total original parts made for content of article no. ",k," is = ",len(original_content_parts))
                    translated_content_parts=[]
                    
                    #translating each part of content
                    try_number = 1
                    for part in original_content_parts:
                        while (1):
                            try:
                                translation = translate_client.translate(part,source_language='en',target_language=code)
                                translated_content_parts.append(translation['translatedText'])
                                break
                            except:
							
                                print("sleeping for 10 seconds due to user limit exceed")
                                if try_number>10:
                                  exit("Error, too much waiting, Translation Server Busy or Internet error.")
                                try_number = try_number + 1
                                time.sleep(10)
                
                    print("Total translated parts made for content of article no. ",k," is = ",len(translated_content_parts))

                    if 'hindi' in language:
                        translated_content = "|".join(translated_content_parts)
                    elif 'bengali' in language:
                        translated_content = "|".join(translated_content_parts)
                    else:
                        translated_content = ".".join(translated_content_parts)
                    
                    
                    '''
                    # tester, ignore.
                    while(1):
                        try:
                            translation = translate_client.translate(content,source_language='en',target_language=code)
                            checker = translation['translatedText']
                            break
                        except:
                            print("sleeping for 10 seconds due to user limit exceed")
                            time.sleep(10)
                    print("SIZE OF TRANSLATED CONTENT IF NOT BREAKED = ",len(checker))
                    print("SIZE OF TRANSLATED CONTENT IF BREAKED = ",len(translated_content))
                    '''
                    
                    string = language + '_database'
                    try:
                        cursor.execute('use main_database')
                        query_string = 'insert ' + string + ' values (%s,%s,%s,%s,%s,%s,%s)'
                        cursor.execute(query_string,(ide,published_date,translated_title,link,source,translated_summary,translated_content))
                        print("article ",i," translated for ",language," language\n")
                    except:
                        continue
                   

            
            
            
            conn.commit()	
            print("ARTICLE NO.",k,"HAS BEEN SUCCCESSFULLY TRANSLATED AND PUSHED INTO DATABASE")
            k=k+1
            
            with open(r'C:\Users\shashank\Desktop\sql_implementation\translated_articles_ids.txt','a') as f:
                f.write('{}\n'.format(ide))
            logging.info('Info: Article successfully translated with id : {}'.format(ide))
    else:
        print("article skipped for translation already translated")

