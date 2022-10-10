from Selenium import Selenium, webdriver


class Base():
    def __init__(self) -> None:
        self.seleniumDriver: webdriver.Chrome or webdriver.Firefox or webdriver.Remote = Selenium.getDriver()
