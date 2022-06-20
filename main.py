from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions as selex
from selenium.webdriver.common.by import By
import datetime
import os
import time
from bitrix import SeoModule

def main():

    start = SeoModule()

    start.run('new_settings_examples.csv')

if __name__ == '__main__':

    main()
