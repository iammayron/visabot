import json

from Auth import Auth
from Base import Base
from Selenium import By


class Request(Base):
    def __init__(self) -> None:
        super().__init__()
        self.Auth = Auth()

    def json(self, url):
        self.seleniumDriver.get(url)
        if not self.Auth.isLoggedIn():
            if self.Auth.loginIfNotBlocked():
                return self.json(url)
        else:
            content = self.seleniumDriver.find_element(By.TAG_NAME, 'pre').text
            return json.loads(content)
