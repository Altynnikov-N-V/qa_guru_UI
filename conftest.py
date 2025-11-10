import os
import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from utils import attach

DEFAULT_BROWSER_VERSION = "128.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='128.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    base_url = os.getenv('BASE_URL')
    browser.config.base_url = base_url
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    url = os.getenv('URL')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{url}/wd/hub",
        options=options
    )
    browser.config.driver = driver

    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open('/')

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
