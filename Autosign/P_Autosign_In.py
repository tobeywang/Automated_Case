import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from datetime import datetime as dt
import json
#System.setProperty("webdriver.ie.driver","C://Program Files (x86)//Internet Explorer//iexplore.exe");
try:
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = "plog_in.log",filemode="w+",level="INFO")
    logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
    logging.info('Start-----')
#    chromedriver = "chromedriver_2.32\\chromedriver.exe"  
    #userID #passWD
    jsonfile='personinfo.json'
    if os.path.exists(jsonfile):
        with open(jsonfile,'r') as js:
            jd=json.load(js)
            user_id=jd["id"]
            pw=jd["pw"]
            driver = webdriver.Chrome()  
            #測試機
            #driver.get("http://10.87.50.11/FKWeb/")
            #正式機
            driver.get("https://go.linyuan.com.tw/FKWeb/")
            
            #userID
            #passWD
            #btn_submit
            time.sleep(2)
            username = driver.find_element_by_id("UID")
            password = driver.find_element_by_id("KEY")
            username.send_keys(user_id)
            password.send_keys(pw)
            driver.find_element_by_id("btnLogin").click()
            logging.info('Login processing----')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='我要簽到']"))).click()
            
            logging.info(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
            logging.info('End-----')    
    else:
        logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
        logging.warning('pls run changePW.py, thanks')  
except Exception as error:
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = "plog_in.log",
    filemode="w",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


#讀登入後的頁面
#time.sleep(10)
#driver.url
#from bs4 import BeautifulSoup
#soup2=BeautifulSoup(driver.page_source,"lxml")
##for ele in soup2.select('.message .section .messageBtn .clip_text'):
    #print(ele.text)
#time.sleep(10)
#簽到
#driver.execute_script("openDialog0600('', '', 'ATNDN_EARLY_RESN');");
#簽退
#driver.execute_script("openDialog0600('', '', 'LEAVE_LATE_RESN');");
#driver.find_element_by_id("checkInBtn").click()
#20171005 調整等待，取span click
#簽到
#==============================================================================
# try :
# 
# except Exception as e:
#     print(e)
#==============================================================================


