from seo_modules_dicts.seo_module_props import folder_props, sections
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
        self.driver.get(self.enter_url)
        self.driver.implicitly_wait(3)
        self._login()

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

class SeoModule(Bitrix):

    def __init__(self):
        self.folder_props = folder_props
        self.sections = sections
        self.page_counter = 1
        super(SeoModule, self).__init__()

    def _load_properties(self, folder):

        self.properties = {}
        with open(self.folder_props[folder], 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                name = line.split(":")[0].lower().strip()
                key = line.split(":")[-1]
                self.properties[name] = key

        return self.properties

    def _load_seo_settings_from_csv(self, settings_file_path):

        self.seo_settings = []

        with open(settings_file_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter = ';', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                self.seo_settings.append(row)

        return self.seo_settings

    def _apply_seo_setting(self):

        self.driver.find_element(By.NAME, 'apply').click()

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
               self.unchosen_properties, self.related_settings_bottom, self.id

    def _page_counter_update(self):

        print(f'Finished {self.page_counter} pages')
        self.page_counter += 1

class AddNewSetting(SeoModule):

    def __init__(self):

        self.new_setting_url = 'https://api.iport.ru/bitrix/admin/zverushki.seofilter_setting_edit.php'
        super(AddNewSetting, self).__init__()

    def add_new_settings(self, settings_file_path, folder):

        self.enter_bitrix()
        self._load_properties(folder)
        self._load_seo_settings_from_csv(settings_file_path)

        for setting in self.seo_settings:

            self._get_data_for_setting(setting)

            try:
                self._create_new_setting()
                self._initial_setting_setup()
                self._setup_cpu()
                self._setup_tag_names()
                self._setup_meta_data()
                self._setup_linking()
                self._choose_properties()
                self._apply_seo_setting()
                self._page_counter_update()
            except Exception as ex:
                print(f'{self.id}')
                print(ex)

    def _create_new_setting(self):

        self.driver.implicitly_wait(2)
        self.driver.get(self.new_setting_url)