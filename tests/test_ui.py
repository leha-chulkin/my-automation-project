import pytest
from selenium import webdriver
from page_objects.example_page import ExamplePage
from configs.env_config import BASE_URL
from time import sleep

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_ui(driver):
    page = ExamplePage(driver)
    page.open()
    page.login("testuser","testpass")

    assert page.is_logged_in()

def test_ui_another_feature(driver):

    driver.get(BASE_URL + "/some_page")

    assert True
