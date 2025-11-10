import os
import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    browser.config.base_url = 'https://playrix.com'
    options = Options()
    options.add_argument('--window-size=1920,1080')

    if os.getenv('HEADLESS') == 'true':
        options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10
    browser.config.hold_browser_open = True
    browser.open('/')

    yield
    browser.quit()