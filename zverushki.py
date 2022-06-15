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

class SendRules:

    def __init__(self):

        # initial settings
        headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={headers}')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_window_size(1920, 1080)
        self.driver.delete_all_cookies()

        with open('login.txt', 'r') as f:
            self.login = f.read().splitlines()
            f.close()

    def _login(self):

        self.driver.get('https://api.iport.ru/bitrix/admin')
        time.sleep(5)
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(self.login[0])
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(self.login[1])
        self.driver.find_element(By.NAME, 'Login').click()
        time.sleep(5)

    def _create_new_setting(self):

        new_setting_url = 'https://api.iport.ru/bitrix/admin/zverushki.seofilter_setting_edit.php?lang=ru'
        self.driver.get(new_setting_url)
        time.sleep(5)

    def _collect_data_for_send(self, data):
        self.id = data['id']
        self.cpu = data['cpu']
        self.folder = data['folder']
        self.card_tag = data['card_tag']
        self.catalog_tag = data['catalog_tag']
        self.header = data['h1']
        self.title = data['meta_title']
        self.description = data['meta_description']
        self.setting_description = data['setting_description']
        self.chosen_properties = data['properties'].split(',')

        return self.cpu, self.folder, self.card_tag, self.catalog_tag, self.header, self.title, self.description, \
               self.setting_description, self.chosen_properties


    def _find_checkboxes(self):
        pass

    def _initial_setting_setup(self):
        time.sleep(2)
        sections = {'iphone': '103', 'mac': '76', 'ipad': '86', 'watch': '115', 'cases': '403', 'bags': '382'}
        choose_info_block = Select(self.driver.find_element(By.NAME, 'IBLOCK_ID'))
        choose_info_block.select_by_value("5")
        folder = Select(self.driver.find_element(By.NAME, 'SECTION_ID'))
        folder.select_by_value(sections[self.folder])
        self.checkboxes = self.driver.find_elements(By.CLASS_NAME, 'adm-designed-checkbox-label')
        self.checkboxes[0].click()
        self.driver.find_element(By.NAME, 'DESCRIPTION').send_keys(self.setting_description)
        time.sleep(2)

    def _setup_cpu(self):

        self.driver.find_element(By.NAME, 'URL_CPU').send_keys(self.cpu)
        time.sleep(1)


    def _setup_tag_names(self):
        self.driver.find_element(By.NAME, "TAG_NAME").send_keys(self.card_tag)
        self.driver.find_element(By.NAME, "TAG_SECTION_NAME").send_keys(self.catalog_tag)
        time.sleep(1)

    def _setup_linking(self):
        # top_links = driver.find_element(By.NAME, "RELATED_SETTING_ID").send_keys('2,3,4')
        # bottom_links = driver.find_element(By.NAME, "RELATED_SETTING_ID2").send_keys('2,3,4')
        pass

    def _setup_meta_data(self):
        self.driver.find_element(By.NAME, "PAGE_TITLE").send_keys(self.header)
        self.driver.find_element(By.NAME, "META_TITLE").send_keys(self.title)
        self.driver.find_element(By.NAME, "META_DESCRIPTION").send_keys(self.description)
        time.sleep(1)

    def _apply(self):
        self.driver.find_element(By.NAME, 'apply').click()
        time.sleep(3)


    def _choose_properties(self):
        self.driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
        for item in self.chosen_properties:
            param = self.driver.find_element(By.ID, self.properties[item])
            param.find_element(By.XPATH, '../..').click()
            time.sleep(1)


    def _load_props(self):

        folder_props = {'watch': 'watch_props_dict.txt'
                     }
        self.properties = {}
        with open(folder_props[self.folder], 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                name = line.split(":")[0].lower().strip()
                key = line.split(":")[-1]
                self.properties[name] = key

        return self.properties

def load_data(file_path: str):

    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in csv_reader:
            data.append(row)

    return data

def main():

    data = load_data('new_settings_template.csv')

    setup_settings = SendRules()

    setup_settings._login()

    for item in data:
        setup_settings._collect_data_for_send(item)
        setup_settings._load_props()
        setup_settings._create_new_setting()
        setup_settings._find_checkboxes()
        setup_settings._initial_setting_setup()
        setup_settings._setup_cpu()
        setup_settings._setup_tag_names()
        setup_settings._setup_meta_data()
        setup_settings._choose_properties()
        setup_settings._apply()

if __name__ == '__main__':
    main()




