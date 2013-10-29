#!./venv/bin/python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Oct 29 11:07:50 2013
"""
## This example reads the different RSS-feeds from 'De Standaard' and puts them in a sqlite-db


import feedparser,requests,re, json, datetime
import sqlite3, logging
from BeautifulSoup import BeautifulSoup

logger = logging.getLogger('feedreader')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR,filename='./data/feedexample.log',filemode='w')

def ExtractPost(content):
    page=BeautifulSoup(content)
    post=page.find('article')('div',{'class':'article__body'})[0](text=True)
    article=' '.join([pst for pst in post])
    return article.replace('\n',' ')

def dbInsert(title,content,date,link,source): 
    # Insert a row of data
    try:
        c.execute("INSERT INTO articles VALUES ('%s','%s','%s','%s','%s')"%(title,content,date,link,source))
        conn.commit()
    except Exception, e:
       logger.error("failed to commit:%s\n%s"%(title,e))

def cleanstr(text):
    return text.replace("'","").replace("`","").replace('"','').replace(",","")
    
    

if __name__ == '__main__':
    settings=json.load(open('config.json','r'))
    sources=settings['sources']
    try:
        lastmodifieds=settings['lastmodifieds']                                #otherwise
    except Exception:
        lastmodifieds=[]                                                       #first run
    conn = sqlite3.connect(settings['db_name'])
    c = conn.cursor()

    for tel in range(len(sources)):
        if len(lastmodifieds)<(tel+1):
            d = feedparser.parse(sources[tel])                                #first run
            lastmodifieds.append(d.modified) 
        else:
            d = feedparser.parse(sources[tel], modified=lastmodifieds[tel])    #otherwise
            lastmodifieds[tel]=d.modified      
        
        logger.info('Begin parsing feed: %s'%(d['feed']['title']))
        for entry in d.entries:
            logger.info('\t'+entry.title)
            try:            
                r = requests.get(entry.link)
                post=ExtractPost(r.content)
            except Exception:
                post=entry.description.replace('<p>','').replace('</p>','')


            dbInsert(cleanstr(entry.title),cleanstr(post),entry.published,entry.link,d['feed']['title'])
        
    settings['lastmodifieds']=lastmodifieds
    json.dump(settings,open('config.json','w'))
    conn.close()