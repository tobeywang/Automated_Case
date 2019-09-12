# win32com 打包exe 用
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from datetime import datetime as dt
import json
from selenium.webdriver.common.keys import Keys
#System.setProperty("webdriver.ie.driver","C://Program Files (x86)//Internet Explorer//iexplore.exe");

#chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"  

try:
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = "plog.log",filemode="w+",level="INFO")
    logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
    logging.info('Start-----')
    #chromedriver = "chromedriver_2.36\\chromedriver.exe"  
    #userID #passWD
    jsonfile='personinfo.json'
    if os.path.exists(jsonfile):
        with open(jsonfile,'r') as js:
            jd=json.load(js)
            user_id=jd["id"]
            pw=jd["pw"]
            logging.info('get user_id'+user_id)
#            os.environ["webdriver.chrome.driver"] = chromedriver  
#            driver = webdriver.Chrome(chromedriver) 
            driver = webdriver.Chrome() 
#            driver.get("http://google.com")
            #測試機
            #driver.get("http://10.87.50.11/FKWeb/")
            #正式機
            driver.get("https://go.linyuan.com.tw/FKWeb/")
#            driver.get("https://w3.cathaylife.com.tw/eai/ZPWeb/login.jsp")
            logging.info('web is opened')
            #btn_submit
            username = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "UID")))
#            username = driver.find_element_by_name("username")
            size=username.size
            password = driver.find_element_by_id("KEY")
#            username.click()
            username.send_keys(user_id)
            password.send_keys(pw)
            password.send_keys(Keys.RETURN)
            driver.find_element_by_id("btnLogin").submit()
            logging.info(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
            logging.info('End-----')
    else:
        logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
        logging.warning('pls run changePW.py, thanks')
except Exception as error:
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = "plog.log",
    filemode="w",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



#讀登入後的頁面
#driver.url
#from bs4 import BeautifulSoup
#soup2=BeautifulSoup(driver.page_source,"lxml")
##for ele in soup2.select('.message .section .messageBtn .clip_text'):
    #print(ele.text)
time.sleep(10)
#簽到
#driver.execute_script("openDialog0600('', '', 'ATNDN_EARLY_RESN');");
#簽退
#driver.execute_script("openDialog0600('', '', 'LEAVE_LATE_RESN');");
#driver.find_element_by_id("checkInBtn").click()
