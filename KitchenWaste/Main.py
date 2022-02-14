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
import sys #查exception
#System.setProperty("webdriver.ie.driver","C://Program Files (x86)//Internet Explorer//iexplore.exe");

#chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"  

try:
    logging.getLogger('').handlers = []
    logging.basicConfig(filename = "run_log.log",filemode="w+",level="INFO")
    logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
    logging.info('Start-----')
#    chromedriver = "chromedriver_2.36\\chromedriver.exe"  
    #userID #passWD
    jsonfile='info.json'
    if os.path.exists(jsonfile):
        with open(jsonfile,'r',encoding='UTF-8') as js:
        #with open(jsonfile,'r') as js:
            #多筆讀取
            logging.info('row Start-----')
            multiple=js.readlines()
            for line in multiple:
                jd=json.loads(line)
                logging.info('row data '+line)
                user_id=jd["id"]
                user_name=jd["name"]
                user_tel=jd["tel"]
                logging.info('get user_id '+user_id)
                #環境變數抓取chromedriver'
    #            os.environ["webdriver.chrome.driver"] = chromedriver  
                #指定chromedriver位置'
    #            driver = webdriver.Chrome(chromedriver) 
                driver = webdriver.Chrome() 
    #            driver.get("http://google.com")
                #測試機
                driver.get("file:///D:/Cathay_T/Python/cr_kitchenwaste/Code/Unit_Test_html/main.html")
                #正式機
#                driver.get("https://kitchenwaste.ksepb.gov.tw/apply.aspx")
                logging.info('web is opened')
                
#                btn_submit
                #xpath
                username = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='王大明']")))
                area =driver.find_element_by_xpath("//input[@value='01']").click()
                userid=driver.find_element_by_xpath("//input[@placeholder='身分證末四碼']")
                usertel=driver.find_element_by_xpath("//input[@placeholder='07-7351500']")
                #element id
#                username = WebDriverWait(driver, 10).until(
#                        EC.presence_of_element_located((By.ID, "tbApplyName")))
#    #            username = driver.find_element_by_name("username")
#                size=username.size
#                userid = driver.find_element_by_id("tbBriefID")
#                usertel = driver.find_element_by_id("tbTel")
#    #            username.click()
                
                username.send_keys(user_name)
                userid.send_keys(user_id)
                usertel.send_keys(user_tel)
                
                logging.info('5秒後送出:'+dt.now().strftime("%Y/%m/%d %H:%M:%S"))
                time.sleep(5)                
                
                usertel.send_keys(Keys.ENTER)
#                driver.find_element_by_xpath("//input[@class='button']").click()
                
                logging.info(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
                logging.info(user_id+' over-----')
                break
            logging.info('End-----')
    else:
        logging.warning(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
except Exception as error:
    error_class = error.__class__.__name__ #取得錯誤類型
    detail = error.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    errMsg = "Error:[{}] {}".format( error_class, detail)
    logging.error(dt.now().strftime("%Y/%m/%d %H:%M:%S"))
    logging.error(errMsg)
    
#    logging.getLogger('').handlers = []
#    logging.basicConfig(filename = "run_log.log",
#    filemode="w",
#    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



#讀登入後的頁面
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
