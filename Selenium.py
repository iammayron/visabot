import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as Wait
from webdriver_manager.chrome import ChromeDriverManager

import config


class Selenium():
    __instance = None
    __driver = None

    def __new__(self, *args, **kwargs):
        if not Selenium.__instance:
            Selenium.__instance = object.__new__(self, *args, **kwargs)
        return Selenium.__instance

    def __init__(self) -> None:
        self.driver: webdriver.Chrome or webdriver.Firefox or webdriver.Remote = None

    @staticmethod
    def getDriver() -> webdriver.Chrome or webdriver.Remote:
        if Selenium.__driver is None:
            localUse = platform.system() == 'Darwin'

            if config.BROWSER == 'chrome':
                options = ChromeOptions()
            else:
                options = FirefoxOptions()

            options.headless = True
            # options.noSandbox = True
            # options.disableGpu = True
            # options.disableExtensions = True

            if localUse:
                if config.BROWSER == 'chrome':
                    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
                else:
                    driver = webdriver.Firefox(options=options)
            else:
                if config.BROWSER == 'chrome':
                    driver = webdriver.Remote(command_executor=config.HUB_ADDRESS,
                                          desired_capabilities=DesiredCapabilities.CHROME)
                else:
                    driver = webdriver.Remote(command_executor=config.HUB_ADDRESS,
                                          desired_capabilities=DesiredCapabilities.FIREFOX)

            Selenium.__driver = driver

        return Selenium.__driver
