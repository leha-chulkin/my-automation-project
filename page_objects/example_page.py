from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExamplePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "http://example.com"

    def open(self):
        self.driver.get(self.url)

    def login(self, username: str, password: str):
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-btn")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

    def is_logged_in(self) -> bool:

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "logout-btn"))
            )
            return True
        except:
            return False
