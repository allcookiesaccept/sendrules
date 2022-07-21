from selenium.webdriver.common.by import By
from bitrix import Bitrix

class ShopPropertiesCleaner(Bitrix):

    def __init__(self):

        super().__init__()
        self.enter_bitrix()

    def _open_properties_list(self):

        self.driver.get('https://api.iport.ru/bitrix/admin/cat_catalog_edit.php?lang=ru&IBLOCK_ID=5')
        prop_tab = self.driver.find_element(By.XPATH, '//div[@class="adm-detail-tabs-block"]//span[@id="tab_cont_edit3"]')
        prop_tab.click()

    def _load_props_ids(self):
        self.props_for_delete = []

        with open('props_for_delete.txt', 'r', encoding='utf-8') as file:
            self.props_for_delete = file.read().splitlines()
            file.close()

        return self.props_for_delete

    def _delete_property(self):

        for prop in self.props_for_delete:
            try:
                property_elements = self.driver.find_elements(By.XPATH, f"//tr[@id='tr_SECTION_PROPERTY_{prop}']//td")

                property_elements[-1].click()
            except Exception as ex:
                print(ex)

    def run(self):

        self._load_props_ids()
        self._open_properties_list()
        self._delete_property()

def main():

    cleaner = ShopPropertiesCleaner()
    cleaner.run()

if __name__ == '__main__':

    main()