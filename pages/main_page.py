from .base_page import BasePage
from selenium.webdriver.common.by import By

class MainPage(BasePage):
    def get_title(self):
        return self.driver.title

    def click_login_button(self):
        login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "login")))
        login_button.click()