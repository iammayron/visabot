import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as Wait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import config


class Selenium:
    __instance = None
    __driver = None

    def __new__(cls, *args, **kwargs):
        if not Selenium.__instance:
            Selenium.__instance = super(
                Selenium, cls).__new__(cls, *args, **kwargs)
        return Selenium.__instance

    def __init__(self) -> None:
        self.__driver: webdriver.Chrome or webdriver.Firefox or webdriver.Remote = None

    @staticmethod
    def kill() -> None:
        Selenium.__driver = None
        Selenium.__instance = None

    @staticmethod
    def getDriver() -> webdriver.Chrome or webdriver.Remote:
        if Selenium.__driver is None:
            localUse = platform.system() == 'Darwin'

            if config.BROWSER == 'chrome':
                options = ChromeOptions()
            else:
                options = FirefoxOptions()

            options.headless = config.HEADLESS

            if localUse:
                if config.BROWSER == 'chrome':
                    # Use the new Service-based initialization
                    driver = webdriver.Chrome(
                        service=ChromeService(ChromeDriverManager().install()),
                        options=options
                    )
                else:
                    # Use the new Service-based initialization for Firefox
                    driver = webdriver.Firefox(
                        service=FirefoxService(GeckoDriverManager().install()),
                        options=options
                    )
            else:
                if config.BROWSER == 'chrome':
                    driver = webdriver.Remote(
                        command_executor=config.HUB_ADDRESS,
                        desired_capabilities=DesiredCapabilities.CHROME
                    )
                else:
                    driver = webdriver.Remote(
                        command_executor=config.HUB_ADDRESS,
                        desired_capabilities=DesiredCapabilities.FIREFOX
                    )

            Selenium.__driver = driver

        return Selenium.__driver
