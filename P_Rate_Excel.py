
# coding: utf-8

# In[1]:

import pandas
dfs=pandas.read_html('http://rate.bot.com.tw/xrt?Lang=zh-TW')
currency=dfs[0]
currency=currency.ix[:,0:5]
currency.columns=[u'幣別',u'現金1',u'現金2',u'即期1',u'即期2']
#add column
from datetime import datetime
currency[u'日期']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
from openpyxl import load_workbook
book = load_workbook(filename ='D:\\Cathay_T\\Python\\PythonSource\\Job\\rate.xlsx')
writer = pandas.ExcelWriter('D:\\Cathay_T\\Python\\PythonSource\\Job\\rate.xlsx', engine='openpyxl')
writer.book=book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#print (len(book.worksheets))
#writer.sheets='Sheet1'
#writer = ExcelWriter('rate.xlsx')
#currency.to_excel(writer,'Sheet1',columns=[u'幣別',u'現金1',u'現金2',u'即期1',u'即期2',u'日期'])
sheetname=datetime.now().strftime('%Y%m%d%H%M%S')
currency.to_excel(writer,sheet_name=sheetname)
writer.save()


# In[ ]:



