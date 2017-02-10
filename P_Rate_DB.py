
# coding: utf-8

# In[11]:

import pandas
dfs=pandas.read_html('http://rate.bot.com.tw/xrt?Lang=zh-TW')
#from bs4 import BeautifulSoup
#soup=BeautifulSoup(dfs[0],'lxml')
currency=dfs[0]
#print (soup.text)


# In[19]:

currency=currency.ix[:,0:5]


# In[20]:

currency


# In[22]:

currency.columns=['幣別','現金1','現金2','即期1','即期2']


# In[23]:

currency


# In[34]:

#add column
from datetime import datetime
currency['日期']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# In[35]:

currency


# In[36]:

#write to sqlite3
import sqlite3
with sqlite3.connect('currency.sqlite') as db:
    df=currency.to_sql('currency',con=db,if_exists='append')


# In[37]:

#read sqlite3
#with sqlite3.connect('currency.sqlite') as db:
    #df=pandas.read_sql('select * from currency',con=db)
    #print (df)


# In[ ]:



