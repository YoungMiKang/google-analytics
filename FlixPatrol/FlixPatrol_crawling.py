# 팀장 이종문님의 코드를 수정하여 작성함.
############################################################
# Package import
############################################################

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


############################################################
# fucntions
############################################################


def create_driver(browser_path, driver_path, website_url):
    '''Create Driver'''
    options = Options()
    options.binary_location = browser_path
    driver = webdriver.Firefox(executable_path=driver_path, options=options)
    driver.get(website_url)
    
    return driver;

def search_elements(driver, type, name, wait_second, loopCount=1):
    '''Search Tag element.

        driver : create_driver() object
        type : selenium.webdriver.common.by object
        name : element type's name / e.g. if <a class="link"> exist in DOM and type is class name, name argument will check between class name and name argument value.
        wait_second : waiting time.
        loopCount : default = 1. => driver will scroll down once.
        
        +) driver will take a time to search element => Time = wait_secound * loopCount
    '''


    for _ in range(loopCount):
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        ##############################################################
        # DOM 의 구조를 보시고 아래 스크립트를 수정해야 합니다. (맨 마지막까지 스크롤 내리기)
        ##############################################################
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        time.sleep(wait_second) # wait_second 만큼 대기
    
    # create wait object
    wait = WebDriverWait(driver, wait_second)
    # after wait_second, find element
    elements = wait.until(EC.presence_of_all_elements_located((type, name)))


    # check element
    # element_size = len(elements)
    # if element_size != 0:
    #     print(f'element\'s size : {element_size}'); # print element list length
    # else:
    #     print("element isn't Exist.");
    
    return elements;


############################################################
# Setting
############################################################

# browser path : 웹 브라우저 위치
# e.g.) browser_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
browser_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# driver path : Selenium 브라우저 Driver 위치
# e.g.) driver_path = r'C:/Users/lg495/Downloads/geckodriver.exe'
driver_path = r'C:\Users\2019A00310\Downloads\geckodriver-v0.33.0-win32\geckodriver.exe'

# Website url : 크롤링할 웹사이트 URL
# e.g.) website_url = 'https://www.naver.com/'
website_url = 'https://flixpatrol.com/top10/streaming/world/today/full/#netflix-1'

# waiting second : 웹페이지 로딩이 완료될 때까지 기다리는 시간.
# e.g.) wait_second = 10; => 10초
wait_second = 10;

# element type
type = By.ID;

# element name
element_name = 'video-title';

# loop cunt
loop_count = 1;


############################################################
# essential process
############################################################

driver = create_driver(browser_path, driver_path, website_url)


############################################################
# custom Programming
############################################################

#elements = search_elements(driver, type, element_name, wait_second, loop_count)

# result = []
# for element in elements:
#     # result.append(element.get_attribute('title'))
#     # result.append(element.text);
#     result.append(element.get_attribute('aria-label'))

title = []
points = []
change = []
countries = []
total = []

element = driver.find_element(By.ID, "netflix-1")
all_tb_groups = element.find_elements(By.CLASS_NAME, "table-group")
for tb_group in all_tb_groups:
    tb = tb_group.find_elements(By.CLASS_NAME, "table-td")
    title.append(tb[2].text)
    points.append(tb[3].text)
    change.append(tb[4].text)
    countries.append(tb[5].text)
    total.append(tb[-1].text)

# driver close
driver.quit()

print("FlixPatrol info cralwing process".center(50, "-"))
print('start.'); print()

# print data
for index in range(len(all_tb_groups)):
    print("id : ", index)
    print(f"title = {title[index]}\npoints = {points[index]}\nchange = {change[index]}\ncountries = {countries[index]}\ntotal = {total[index]}")
    print(".\n.")

print("Complete.")


############################################################
# Create csv file
############################################################

import pandas as pd
from pathlib import Path 

df = pd.DataFrame({'title': title,
                    'points': points,
                    'change': change,
                    'countries' : countries,
                    'total' : total
                })

file_name = 'FlixPatrol_crawl.csv'

df.to_csv(file_name, encoding="utf-8-sig")
