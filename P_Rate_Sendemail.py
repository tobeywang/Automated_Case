# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:52:31 2019
取得最新的匯率走勢圖
@author: TobeyWang
"""
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header

try:
    smtpObj = smtplib.SMTP("10.1.1.238")
    message = MIMEText('python 測試', 'html', "utf-8")
    message['From'] = Header("admin@cathaysite.com.tw")   # 发送者
    message['To'] =  Header("tobeywang@cathaysite.com.tw")        # 接收者
    subject = 'Python SMTP 測試郵件'
    message['Subject'] = Header(subject, "utf-8")
    
    smtpObj.sendmail("admin@cathaysite.com.tw", ["tobeywang@cathaysite.com.tw"], message.as_string())
    print("發送成功")
except smtplib.SMTPException:
    print ("Error: 無法發送")
"""    
    
#send pic 
import pandas    
import sqlite3
import matplotlib.pyplot as plt
import os 
with sqlite3.connect('D:\Cathay_T\Python\currency.sqlite') as db:
    df_jpy=pandas.read_sql("SELECT 現金1 as cash_in,現金2 as cash_out,即期1 as real_in,即期2 as real_out,日期 FROM currency where 幣別 like '%jpy%' order by 日期 desc limit 180",con=db)
    df_usd=pandas.read_sql("SELECT 現金1 as cash_in,現金2 as cash_out,即期1 as real_in,即期2 as real_out,日期  FROM currency where 幣別 like '%usd%' order by 日期 desc limit 180",con=db)
    df_cny=pandas.read_sql("SELECT 現金1 as cash_in,現金2 as cash_out,即期1 as real_in,即期2 as real_out,日期  FROM currency where 幣別 like '%cny%' order by 日期 desc limit 180",con=db)
df_jpy.index=pandas.to_datetime(df_jpy.日期,format="%Y%m%d %H:%M:%S")
df_jpy.cash_in=df_jpy.cash_in.astype(float)
df_jpy.cash_out=df_jpy.cash_out.astype(float)
df_jpy.real_in=df_jpy.real_in.astype(float)
df_jpy.real_out=df_jpy.real_out.astype(float)

line_jpy=df_jpy.plot(kind="line",y=[r"cash_in",r"cash_out",r"real_in",r"real_out"])
fig = line_jpy.get_figure()
if os.path.isfile("line_jpy.png"):
    os.remove("line_jpy.png") 
fig.savefig("line_jpy.png")

df_usd.index=pandas.to_datetime(df_usd.日期,format="%Y%m%d %H:%M:%S")
df_usd.cash_in=df_usd.cash_in.astype(float)
df_usd.cash_out=df_usd.cash_out.astype(float)
df_usd.real_in=df_usd.real_in.astype(float)
df_usd.real_out=df_usd.real_out.astype(float)

line_usd=df_usd.plot(kind="line",y=[r"cash_in",r"cash_out",r"real_in",r"real_out"])
fig = line_usd.get_figure()
if os.path.isfile("line_usd.png"):
   os.remove("line_usd.png") 
fig.savefig("line_usd.png")

df_cny.index=pandas.to_datetime(df_cny.日期,format="%Y%m%d %H:%M:%S")
df_cny.cash_in=df_cny.cash_in.astype(float)
df_cny.cash_out=df_cny.cash_out.astype(float)
df_cny.real_in=df_cny.real_in.astype(float)
df_cny.real_out=df_cny.real_out.astype(float)

line_cny=df_cny.plot(kind="line",y=[r"cash_in",r"cash_out",r"real_in",r"real_out"])
fig = line_cny.get_figure()
if os.path.isfile("line_cny.png"):
   os.remove("line_cny.png") 
   
fig.savefig("line_cny.png")
    
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

graphs=["line_jpy.png","line_usd.png","line_cny.png"]
template = (''
    '<img src="{graph_url}.png">' 
    '<br>'
'')
#email_body = ''
#for graph in graphs:
#    _ = template
#    _ = _.format(graph_url=graph, caption='')
#    email_body += _

msgText=""
try:
    smtpObj = smtplib.SMTP("10.1.1.238")
    body="test"
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = Header( 'Python SMTP 匯率通知', "utf-8")
    msgRoot['From'] = "admin@cathaysite.com.tw"
    msgRoot['To'] = "tobeywang@cathaysite.com.tw"
    msgRoot.preamble = 'This is a multi-part message in MIME format.'
    
    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    
    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)
    text=""
    for graph in graphs:
        text=text+'<b>%s<b><br><img src="cid:%s"><br>' % (graph,graph)
    msgText = MIMEText(text, 'html')
    msgAlternative.attach(msgText)
    
    # This example assumes the image is in the current directory
    
    for graph in graphs:
        fp = open(graph, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<{}>'.format(graph))
        msgRoot.attach(msgImage) 
   
#        
#    msg_txt=MIMEText('<b>test</b><br><img src="cid:image"><br>' , 'html')  
#    msg.attach(msg_txt)    
#    msg['From'] = Header("admin@cathaysite.com.tw")   # 发送者
#    msg['To'] =  Header("tobeywang@cathaysite.com.tw")        # 接收者
#    subject = 'Python SMTP 測試郵件'
#    msg['Subject'] = Header(subject, "utf-8")
    
#    print(msgRoot.as_string())
    smtpObj.sendmail("admin@cathaysite.com.tw", ["tobeywang@cathaysite.com.tw"], msgRoot.as_string())
    print("發送成功")
except smtplib.SMTPException:
    print ("Error: 無法發送")