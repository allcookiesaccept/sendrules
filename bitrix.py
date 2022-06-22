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

    def enter_bitrix(self):
        self._get_account_data()
        url = self.login[4]
        self.driver.get(url)
        time.sleep(2)

        self._login()

    def _get_account_data(self):

        with open('login.txt', 'r') as f:
            self.login = f.read().splitlines()
            f.close()

        return self.login

    def _login(self):

        client_name = self.login[0]
        pswd = self.login[1]
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(client_name)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(pswd)
        self.driver.find_element(By.NAME, 'Login').click()
        time.sleep(3)

class SeoModule(Bitrix):

    def __init__(self):
        self.folder_props = folder_props
        self.sections = sections
        super().__init__()

    def _load_props(self):

        self.properties = {}
        with open(self.folder_props[self.folder], 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                name = line.split(":")[0].lower().strip()
                key = line.split(":")[-1]
                self.properties[name] = key

        return self.properties

    def _get_data_for_setting(self, data):
        self.id = data['id']
        self.cpu = data['cpu']
        self.folder = data['folder']
        self.card_tag = data['card_tag']
        self.catalog_tag = data['catalog_tag']
        self.header = data['h1']
        self.title = data['meta_title']
        self.description = data['meta_description']
        self.setting_description = data['setting_description']
        self.chosen_properties = data['properties'].split('.')
        self.unchosen_properties = data['un_properties'].split('.')
        self.related_settings_top = data['related_settings_top']
        self.related_settings_bottom = data['related_settings_bottom']

        return self.cpu, self.folder, self.card_tag, self.catalog_tag, self.header, self.title, self.description, \
               self.setting_description, self.chosen_properties, self.related_settings_top, \
               self.unchosen_properties, self.related_settings_bottom

    def _create_new_setting(self):

        new_setting_url = self.login[3]
        self.driver.get(new_setting_url)
        time.sleep(2)

    def _initial_setting_setup(self):

        time.sleep(0.5)
        Select(self.driver.find_element(By.NAME, 'IBLOCK_ID')).select_by_value("5")
        Select(self.driver.find_element(By.NAME, 'SECTION_ID')).select_by_value(self.sections[self.folder])
        self.driver.find_elements(By.CLASS_NAME, 'adm-designed-checkbox-label')[0].click()
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
        self.driver.find_element(By.NAME, "RELATED_SETTING_ID").send_keys(self.related_settings_top)
        self.driver.find_element(By.NAME, "RELATED_SETTING_ID2").send_keys(self.related_settings_bottom)

    def _setup_meta_data(self):
        self.driver.find_element(By.NAME, "PAGE_TITLE").send_keys(self.header)
        self.driver.find_element(By.NAME, "META_TITLE").send_keys(self.title)
        self.driver.find_element(By.NAME, "META_DESCRIPTION").send_keys(self.description)
        time.sleep(1)

    def _choose_properties(self):

        self.driver.execute_script("window.scrollTo(1200, document.body.scrollHeight);")

        time.sleep(2)
        for item in self.chosen_properties:
            param = self.driver.find_element(By.XPATH, f"//label[@for='{self.properties[item]}']//label[@for='{self.properties[item]}']")
            self.driver.execute_script("arguments[0].click();", param)

            time.sleep(1)

    def _apply(self):
        self.driver.find_element(By.NAME, 'apply').click()
        time.sleep(3)

    def _edit_setting(self):

        setting_url = f'{self.login[3]}{self.id}&lang=ru'
        self.driver.get(setting_url)
        time.sleep(5)

    def _replace_cpu(self):

        cpu_field = self.driver.find_element(By.NAME, 'URL_CPU')
        cpu_field.clear()
        cpu_field.send_keys(self.cpu)
        time.sleep(1)

    def _replace_tag_names(self):
        tag_name = self.driver.find_element(By.NAME, "TAG_NAME")
        tag_name.clear()
        tag_name.send_keys(self.card_tag)
        tag_section_name = self.driver.find_element(By.NAME, "TAG_SECTION_NAME")
        tag_section_name.clear()
        tag_section_name.send_keys(self.catalog_tag)
        time.sleep(1)

    def _replace_linking(self):
        top_links = self.driver.find_element(By.NAME, "RELATED_SETTING_ID")
        top_links.clear()
        top_links.send_keys(self.related_settings_top)
        bottom_links = self.driver.find_element(By.NAME, "RELATED_SETTING_ID2")
        bottom_links.clear()
        bottom_links.send_keys(self.related_settings_bottom)

    def _replace_meta_data(self):
        header = self.driver.find_element(By.NAME, "PAGE_TITLE")
        header.clear()
        header.send_keys(self.header)
        meta_title = self.driver.find_element(By.NAME, "META_TITLE")
        meta_title.clear()
        meta_title.send_keys(self.title)
        meta_description = self.driver.find_element(By.NAME, "META_DESCRIPTION")
        meta_description.clear()
        meta_description.send_keys(self.description)

    def _remove_properties(self):

        self.driver.execute_script("window.scrollTo(1200, document.body.scrollHeight);")
        time.sleep(1)
        for item in self.unchosen_properties:
            param = self.driver.find_element(By.XPATH, f"//label[@for='{self.properties[item]}']//label[@for='{self.properties[item]}']")
            self.driver.execute_script("arguments[0].click();", param)
            time.sleep(1)

    def _load_settings(self, settings_file_path):

        self.seo_settings = []

        with open(settings_file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter = ';', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                self.seo_settings.append(row)

        return self.seo_settings

    def run(self, settings_file_path):

        self.enter_bitrix()
        self._load_settings(settings_file_path)

        for setting in self.seo_settings:
            self._get_data_for_setting(setting)
            if setting['id'] == '':
                self._load_props()
                self._create_new_setting()
                self._initial_setting_setup()
                self._setup_cpu()
                self._setup_tag_names()
                self._setup_meta_data()
                self._setup_linking()
                self._choose_properties()
                self._apply()
            else:
                # self._load_props()
                self._edit_setting()
                # self._replace_cpu()
                # self._replace_tag_names()
                # self._replace_meta_data()
                self._replace_linking()
                # self._remove_properties()
                # self._choose_properties()
                self._apply()
