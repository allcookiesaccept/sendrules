from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time
import csv
from selenium.webdriver.common.keys import Keys
from seo_modules_dicts.seo_module_props import folder_props, sections

class Bitrix:

    def __init__(self):

        self.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument(f'user-agent={self.headers}')
        self.driver = webdriver.Firefox(executable_path='d:\\drivers\\geckodriver\\geckodriver.exe')
        self.driver.delete_all_cookies()
        self.driver.set_window_size(1920, 1080)
        self.bitrix_url = 'https://api.iport.ru/bitrix/admin'


    def enter_bitrix(self):

        self._get_account_data()
        self.driver.get(self.enter_url)
        self.driver.implicitly_wait(3)
        self._login()
        time.sleep(3)

    def _get_account_data(self):

        with open('login.txt', 'r') as f:
            self.login = f.read().splitlines()
            f.close()

        self.enter_url = self.login[4]
        self.login_name = self.login[0]
        self.pswd = self.login[1]

        return self.enter_url, self.login_name, self.pswd

    def _login(self):

        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(self.login_name)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(self.pswd)
        self.driver.find_element(By.NAME, 'Login').click()

def main():

    bitrix = Bitrix()
    bitrix.enter_bitrix()

if __name__ == '__main__':

    main()