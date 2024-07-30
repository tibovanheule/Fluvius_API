import json
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver


class Token:

    def __init__(self, login: str, password: str, browser: Union[str | None]):
        self.login = login
        self.password = password
        self.access_token = None
        self.get_token(browser)

    def get_token(self, browser=None):
        if browser is not None:
            browser = browser.lower().strip()
        match browser:
            case "edge":
                # Initialize Edge WebDriver with performance logging enabled
                browser_options = webdriver.EdgeOptions()
            case "firefox":
                # Initialize Firefox WebDriver with performance logging enabled
                browser_options = webdriver.FirefoxOptions()
            case "chrome":
                # Initialize Chrome WebDriver with performance logging enabled
                browser_options = webdriver.ChromeOptions()
                browser_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            case _:
                browser_options = webdriver.ChromeOptions()
        browser_options.add_argument('--enable-logging')
        browser_options.add_argument('--log-level=0')
        browser_options.add_argument('--headless')

        seleniumwire_options = {'enable_har': True}

        match browser:
            case "edge":
                # Initialize Edge WebDriver with performance logging enabled
                driver = webdriver.Edge(options=browser_options, seleniumwire_options=seleniumwire_options)
            case "firefox":
                driver = webdriver.Firefox(options=browser_options, seleniumwire_options=seleniumwire_options)
            case "chrome":
                driver = webdriver.Chrome(options=browser_options, seleniumwire_options=seleniumwire_options)
            case _:
                driver = webdriver.Chrome(options=browser_options, seleniumwire_options=seleniumwire_options)

        # Open the login page
        driver.get('https://mijn.fluvius.be')

        # log_entries = driver.get_log("performance")

        # Wait for the button to be clickable
        WebDriverWait(driver, 100).until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="b2c-account-type-selection-button-personal"]'))).click()

        # Wait for the email input field to be visible
        email_input = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, 'signInName')))

        # Enter the email and password
        email_input.send_keys(self.login)
        driver.find_element(By.ID, "password").send_keys(self.password)

        # Click the login button
        driver.find_element(By.ID, 'next').click()

        # Wait for the page to load and get the cookies
        WebDriverWait(driver, 5000).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="fluv-cookies-button-accept-all"]'))).click()

        data = json.loads(driver.har)

        # Initialize a variable to store the authorization header
        auth_header = None

        # Loop through each entry in the log
        for entry in data['log']['entries']:
            # Loop through each header in the request
            for header in entry['request']['headers']:
                # Check if the header name is 'authorization' and starts with 'Bearer e'
                if header['name'] == 'authorization' and header['value'].startswith('Bearer e'):
                    # If so, store it in our variable and break the loop
                    self.access_token = header['value']
                    break
            # Break the outer loop if we found an authorization header
            if self.access_token is not None:
                break

        driver.quit()
