from selenium.webdriver.common.by import By
import time
import csv
from seo_modules_dicts.seo_module_props import folder_props, sections
from bitrix import Bitrix

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

    def add_new_settings(self, settings_file_path, folder):

        self.enter_bitrix()
        self._load_properties(folder)
        self._load_seo_settings_from_csv(settings_file_path)

        for setting in self.seo_settings:

            self._get_data_for_setting(setting)

            try:
                self._create_new_setting()
                self._add_setting_description()
                self._setting_cpu()
                self._setting_header()
                self._setting_meta_title()
                self._setting_meta_description()
                self._setting_product_tag_name()
                self._setting_catalog_tag_name()
                self._choose_properties()
                self._apply_seo_setting()
                self._page_counter_update()
            except Exception as ex:
                print(f'{self.id}')
                print(ex)

    def edit_settings(self, settings_file_path, folder):

        self.enter_bitrix()
        self._load_properties(folder)
        self._load_seo_settings_from_csv(settings_file_path)

        for setting in self.seo_settings:

            self._get_data_for_setting(setting)

            try:
                self._open_existing_setting()
                # self._add_setting_description()
                # self._setting_header()
                # self._setting_meta_title()
                # self._setting_meta_description()
                # self._setting_product_tag_name()
                # self._setting_catalog_tag_name()
                self._setting_top_linking()
                self._setting_bottom_linking()
                # self._remove_properties()
                # self._choose_properties()
                self._apply_seo_setting()
                self._page_counter_update()

            except Exception as ex:
                print(f'{self.id}')
                print(ex)

    def _create_new_setting(self):

        self.driver.get(f'{self.new_setting_url}{self.sections[self.folder]}')
        time.sleep(2)
        print(f'Creating {self.header}')
        self._click_site_checkbox()

    def _click_site_checkbox(self):

        self.driver.find_elements(By.CLASS_NAME, 'adm-designed-checkbox-label')[0].click()
        time.sleep(0.5)

    def _add_setting_description(self):

        print(f'Setting description {self.cpu}')

        description = self.driver.find_element(By.NAME, 'DESCRIPTION')
        description.clear()
        description.send_keys(self.setting_description)

    def _setting_top_linking(self):

        print(f'Setting top links for {self.cpu}')

        top_links = self.driver.find_element(By.NAME, "RELATED_SETTING_ID")
        top_links.clear()
        top_links.send_keys(self.related_settings_top)

    def _setting_bottom_linking(self):

        print(f'Setting bottom links for {self.cpu}')

        bottom_links = self.driver.find_element(By.NAME, "RELATED_SETTING_ID2")
        bottom_links.clear()
        bottom_links.send_keys(self.related_settings_bottom)

    def _setting_cpu(self):

        print(f'Adding setting url')

        cpu_field = self.driver.find_element(By.NAME, 'URL_CPU')
        cpu_field.clear()
        cpu_field.send_keys(self.cpu)

    def _setting_header(self):

        print('Adding Header')

        header = self.driver.find_element(By.NAME, "PAGE_TITLE")
        header.clear()
        header.send_keys(self.header)

    def _setting_meta_title(self):

        print('Adding Title')

        meta_title = self.driver.find_element(By.NAME, "META_TITLE")
        meta_title.clear()
        meta_title.send_keys(self.title)

    def _setting_meta_description(self):

        print('Adding Meta Description')

        meta_description = self.driver.find_element(By.NAME, "META_DESCRIPTION")
        meta_description.clear()
        meta_description.send_keys(self.description)

    def _setting_product_tag_name(self):

        print('Adding Product Tag Name')

        tag_name = self.driver.find_element(By.NAME, "TAG_NAME")
        tag_name.clear()
        tag_name.send_keys(self.card_tag)

    def _setting_catalog_tag_name(self):

        print('Adding Catalog Tag Name')

        tag_section_name = self.driver.find_element(By.NAME, "TAG_SECTION_NAME")
        tag_section_name.clear()
        tag_section_name.send_keys(self.catalog_tag)

    def _choose_properties(self):

        self.driver.execute_script("window.scrollTo(1200, document.body.scrollHeight);")
        print('Setting properties')
        for item in self.chosen_properties:
            self.driver.implicitly_wait(3)
            param = self.driver.find_element(By.XPATH, f"//div[@class='checkbox']//label[@for='{self.properties[item]}']//span[@class='bx-filter-input-checkbox']//label[@for='{self.properties[item]}']")
            self.driver.implicitly_wait(3)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", param)
            self.driver.implicitly_wait(3)
            self.driver.execute_script("arguments[0].click();", param)
            time.sleep(0.5)

    def _remove_properties(self):

        self.driver.execute_script("window.scrollTo(1200, document.body.scrollHeight);")
        time.sleep(1)
        for item in self.unchosen_properties:
            param = self.driver.find_element(By.XPATH, f"//div[@class='checkbox']//label[@for='{self.properties[item]}']//span[@class='bx-filter-input-checkbox']//label[@for='{self.properties[item]}']")
            self.driver.execute_script("arguments[0].click();", param)
            time.sleep(1)

    def _open_existing_setting(self):

        setting_url = f'{self.edit_setting_url}{self.id}'
        self.driver.get(setting_url)


def main():

    file = 'pitanie_kabeli_25072022_linking.csv'

    service = SeoModule()

    service.edit_settings(file, 'Питание и кабели')

if __name__ == '__main__':

    main()