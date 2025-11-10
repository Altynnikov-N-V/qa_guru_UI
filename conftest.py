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
        action='store',
        default=DEFAULT_BROWSER_VERSION,
        help='Browser version for Selenoid'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


def is_ci_environment():
    return os.getenv('CI') == 'true' or os.getenv('JENKINS_HOME') is not None


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    base_url = os.getenv('BASE_URL', 'https://playrix.com')
    browser.config.base_url = base_url

    browser_version = request.config.getoption('--browser_version')

    options = Options()

    if is_ci_environment():
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

        if login and password and url:
            driver = webdriver.Remote(
                command_executor=f"https://{login}:{password}@{url}/wd/hub",
                options=options
            )
        else:
            print("CI environment detected but Selenoid credentials not found. Using local ChromeDriver.")
            driver = setup_local_chrome(options)
    else:
        driver = setup_local_chrome(options)

    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10
    browser.config.hold_browser_open = False

    browser.open('/')

    yield browser

    if is_ci_environment() or os.getenv('ATTACH_ARTIFACTS', 'false').lower() == 'true':
        attach.add_screenshot(browser)
        attach.add_logs(browser)
        attach.add_html(browser)
        if is_ci_environment():
            attach.add_video(browser)

    browser.quit()


def setup_local_chrome(options):
    options.add_argument('--window-size=1920,1080')

    if os.getenv('HEADLESS', 'false').lower() == 'true':
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(options=options)