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
import pandas as pd
import json

class Browser:

    def __init__(self):

        self.options = webdriver.ChromeOptions()
        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options.add_argument(f'user-agent={headers}')
        self.options.add_argument("--auto-open-devtools-for-tabs")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def open_url(self, url):

        self.url = url
        self.driver.get(self.url)
        time.sleep(5)


class ListingProperties(Browser):

    def __init__(self):
        self.properties_db = {}

        super().__init__()

    def _get_header(self):

        self.header = self.driver.find_element(By.TAG_NAME, 'h1').text.split(' - ')[0]
        return self.header

    def _get_properties(self):

        self.properties = self.driver.execute_script("return window.catalogState")

        return self.properties

    def _add_properties_to_dict_list(self):

        self.props_list = []

        for prop in self.properties:
            prop_line = {}
            prop_line[prop['ID']] = [prop['NAME'], prop['CODE']]
            self.props_list.append(prop_line)

        return self.props_list

    def _add_properties_to_db(self):

        self.properties_db[self.header] = self.props_list

    def _save_to_file(self):

        with open('props.txt', 'w', encoding='utf-8') as file:
            for line, value in self.properties_db.items():
                for item in value:
                    for k, v in item.items():
                        file.write(f'{line}: {k} {v}\n')

    def run(self, urls):

        for url in urls:
            try:
                self.open_url(url)
                self._get_header()
                self._get_properties()
                self._add_properties_to_dict_list()
                self._add_properties_to_db()
            except Exception as ex:
                print(ex)

        self._save_to_file()


if __name__ == '__main__':

    local = 'https://localssr.iport.ru:3000/catalog/'

    paths = []

    with open('groups.txt', 'r') as file:
        slugs = file.read().splitlines()
        for slug in slugs:
            paths.append(f"{slug}/")

    urls = []
    property_checker = ListingProperties()

    for path in paths:
        urls.append(f'{local}{path}')

    property_checker.run(urls)