import platform

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
        self.driver: webdriver.Chrome or webdriver.Remote = None

    @staticmethod
    def getDriver() -> webdriver.Chrome or webdriver.Remote:
        if Selenium.__driver is None:
            localUse = platform.system() == 'Darwin'

            options = Options()
            # options.headless = True
            # options.noSandbox = True
            # options.disableGpu = True
            # options.disableExtensions = True

            if localUse:
                driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=options)
            else:
                driver = webdriver.Remote(command_executor=config.HUB_ADDRESS,
                                          desired_capabilities=DesiredCapabilities.CHROME)

            Selenium.__driver = driver

        return Selenium.__driver
