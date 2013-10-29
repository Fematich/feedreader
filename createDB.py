#!./venv/bin/python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Oct 29 12:35:42 2013
"""
import json,sqlite3

def setupDB():
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE articles
             (title text, content text, date text, link text UNIQUE,source text)''')

    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    

if __name__ == '__main__':
    dbname='data/articles.db'
    settings=json.load(open('config.json','r'))
    settings['db_name']=dbname
    setupDB()
    json.dump(settings,open('config.json','w'))