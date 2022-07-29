import time

from bitrix import Bitrix
from selenium.webdriver.common.by import By


class SitemapUpdater(Bitrix):

    def __init__(self):
        super(SitemapUpdater, self).__init__()

    def run(self):

        self.enter_bitrix()
        self._open_sitemap_settings()
        self._find_update_buttons()
        self._click_update_buttons()
        time.sleep(3)
        self.close_bitrix()


    def _open_sitemap_settings(self):

        self.driver.get(self.sitemap_settings_url)

    def _find_update_buttons(self):

        self.update_buttons = \
            self.driver.find_elements(By.NAME, 'save')

        return self.update_buttons

    def _click_update_buttons(self):

        for button in self.update_buttons:
            button.click()

def main():

    updater = SitemapUpdater()
    updater.run()

if __name__ == '__main__':

    main()