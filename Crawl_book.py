# -*- coding: utf-8 -*-
"""
Created on Thu May 17 17:40:18 2018

@author: TobeyWang
"""

import requests
from bs4 import BeautifulSoup
import os
url='your book website'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
i=0
folder_1='' #類型
folder_2='' #書名
table1=soup.find('table').find('table').find('table')
for link in table1.find_all('a'):
    #小說類型
    href=link.get('href')
    text=link.get_text()
    folder_1=text
    #指定類型小說下載(不想所有小說都下載)
    if(text=='懸疑小說'):
        '''建立最外層資料夾'''
        if not os.path.exists('books\\'+folder_1):
            os.makedirs('books\\\\'+folder_1)
        booksresponse=requests.get(url+href)    
        '''分頁'''
        p=href.find("P=")
        key=href[p+2:]
        for page in range(20):
            if(page>0):
                href='?M=hd&P='+key+'_'+str(page+1)
                booksresponse=requests.get(url+href)
                soup = BeautifulSoup(booksresponse.text, 'lxml')   
                strong=soup.find('strong')
                if(strong is not None and strong.text.find('404')>=0):
                    break #分頁開啟失敗，就結束
            #網頁開啟OK 開始撈書
            div=soup.find('div')
            #抓這頁的書
            for link in div.find_all('a'):
                href=link.get('href')
                text=link.get_text()
                if(text!='' and text!=None):
                    folder_2=text #書名
                    signbook=requests.get(url+href) 
                    soup3 = BeautifulSoup(signbook.text, 'lxml')
                    for but in soup3.find('table').find_all('input',type='button'):
                        values=but.get('value')
                        onclick=but.get('onclick')
                        if(values.find('epub')>0 and values.find(r'直式')==-1):
                            start=onclick.find("('")
                            end=onclick.find("')")
                            no=onclick[start+2:end]
                            download=requests.get(url+'?M=d&P='+no+'.epub')
                            print(url+'?M=d&P='+no+'.epub')
                            #確定下載頁再做移動
                            if(download.status_code==200):
                                with open('books\\'+folder_1+'\\'+folder_2+'.epub','wb') as wd:
                                    wd.write(download.content)
        