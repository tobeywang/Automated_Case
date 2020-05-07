
# coding: utf-8
import sqlite3
import requests
import pandas
import logging
from bs4 import BeautifulSoup
from datetime import date,timedelta
from datetime import datetime

def get_Single_Volume(westdate):
    #第一次建立db與table
    with sqlite3.connect('../../finance.sqlite') as db:
        #是否轉過
        df=pandas.read_sql('select strftime("%Y%m%d",匯入日期) as 日期 from MI_INDEX20 order by 匯入日期 desc LIMIT 1',con=db)
    lastdate=''
    if len(df)==1:
     lastdate=str(df["日期"][0])
    today=str(westdate).replace('-','')
    message=''
    #撈取證交所提供的資料下載功能連結
    if lastdate!=today:
     url='http://www.twse.com.tw/exchangeReport/MI_INDEX20?response=html&date={0}'
     url=url.format(today)
     print(url)
     #確定是否有table
     try:
      dfs=pandas.read_html(url)
      ff=dfs[0]
      ff.columns=['排名','證券代號','證券名稱','成交股數','成交筆數','開盤價','最高價','最低價','收盤價','漲跌','漲跌價差','最後買價','最後賣價']
      #add column
      ff['匯入日期']= datetime.strptime(westdate, '%Y-%m-%d')
      #print(ff)
      #寫入資料庫
      df=ff.to_sql('MI_INDEX20',con=db,if_exists='append')
      message='Successful'
     except:
      message='no data'
     return message
def getdate():
    today=date.today()
    datearr=str(today).split('-')
    #陣列
    twdate='%2F'.join ([str(int(datearr[0])-1911),datearr[1],datearr[2]])
    return twdate     
def get_Stock_list():
    #http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
    #http://isin.twse.com.tw/isin/C_public.jsp?strMode=4
    #抓取資料
    dfs=pandas.read_html('http://isin.twse.com.tw/isin/C_public.jsp?strMode=2',encoding = 'big5',header=0 )
    result=dfs[0]
    newds=list(get_dataframe(result))
    #axis:0 index
    ds2=pandas.concat(newds,axis=0)
    with sqlite3.connect('finance.sqlite') as db:
     df=ds2.to_sql('MI_STOCK',con=db,if_exists='replace')
    print(ds2)
def get_dataframe(result):
    columns = ['代號','名稱', 'ISIN','上市日','市場別','產業別','CFICode']
    for index in range(len(result)):
        s_name=str(result.iloc[index]['有價證券代號及名稱'])
        if(str(s_name)=='股票'):
            continue;
        elif(str(s_name)=='上市認購(售)權證'):
            break;  
        #寫入newdf
        #print(s_name)
        id,name=str(s_name).split()
        d = { '代號': [id],'名稱': [name],'ISIN': [result.iloc[index]['國際證券辨識號碼(ISIN Code)']],
             '上市日': [result.iloc[index]['上市日']],'市場別': [result.iloc[index]['市場別']],
             '產業別': [result.iloc[index]['產業別']],'CFICode': [result.iloc[index]['CFICode']]}
        yield pandas.DataFrame(data=d,columns=columns)
def main():
	#start=date(2017,12,1)
	#end=date(2018,1,1)
	#delta = end - start
	#cu=start
	#import datetime
	#for y in range(delta.days):
     #cu=start+timedelta(days=y)
    westdate='2017-12-15'
    messages=get_Single_Volume(westdate)
    #if message!='Successful':
    print (messages)
if __name__== "__main__":
    main()
    
#網址清單
#依日期 個股日本益比、殖利率及股價淨值比(有分頁)
#http://www.twse.com.tw/zh/page/trading/exchange/BWIBBU_d.html
#依日期 三大法人買賣超日報
#http://www.twse.com.tw/zh/page/trading/fund/T86.html
#依個股、日期 每日成交資訊
#http://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html