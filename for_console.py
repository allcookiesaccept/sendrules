import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
from selenium.webdriver.support.ui import Select

headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={headers}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

with open('login.txt', 'r') as f:
    login = f.read().splitlines()
    f.close()

login_url = 'https://api.iport.ru/bitrix/admin'
driver.get(url=login_url)
time.sleep(2)
driver.find_element(By.NAME, 'USER_LOGIN').send_keys(login[0])
driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(login[1])
driver.find_element(By.NAME, 'Login').click()
time.sleep(2)

new_setting_url = 'https://api.iport.ru/bitrix/admin/zverushki.seofilter_setting_edit.php?lang=ru'

driver.get(new_setting_url)
time.sleep(2)


choose_info_block = Select(driver.find_element(By.NAME, 'IBLOCK_ID'))
choose_info_block.select_by_value("5")
folder = Select(driver.find_element(By.NAME, 'SECTION_ID'))
folder.select_by_value('76')
checkboxes = driver.find_elements(By.CLASS_NAME, 'adm-designed-checkbox-label')
checkboxes[0].click()
time.sleep(2)