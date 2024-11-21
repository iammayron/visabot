import random
import time

import config
from Base import Base
from Selenium import EC, By, Wait


class Auth(Base):
    def goToLoginPage(self):
        self.seleniumDriver.get(config.BASE_URL)
        time.sleep(1)

        # TODO
        # Verifica se o usuário está logado procurando belo botão "Continuar" encontrado na página de grupos
        # continueButton = self.seleniumDriver.find_elements(
        #     By.XPATH, "//a[contains(text(),'" + config.CONTINUE_BUTTON_TEXT + "')][contains(@class, 'primary')]")
        # if len(continueButton):
        #     return getJsonList()

        self.seleniumDriver.find_element(
            By.XPATH, '//a[@class="down-arrow bounce"]').click()
        time.sleep(1)

        self.seleniumDriver.find_element(
            By.XPATH, '//*[@id="main"]/div[2]/div[3]/div[2]/div[1]/div/a').click()
        time.sleep(1)
        Wait(self.seleniumDriver, 60).until(
            EC.presence_of_element_located((By.NAME, "commit")))

        self.seleniumDriver.find_element(
            By.XPATH, '//a[@class="down-arrow bounce"]').click()
        time.sleep(1)

    def login(self):
        self.goToLoginPage()

        self.seleniumDriver.find_element(
            By.ID, 'user_email').send_keys(config.EMAIL)
        time.sleep(random.randint(1, 3))

        self.seleniumDriver.find_element(
            By.ID, 'user_password').send_keys(config.PASSWORD)
        time.sleep(random.randint(1, 3))

        self.seleniumDriver.find_element(By.CLASS_NAME, 'icheckbox').click()
        time.sleep(random.randint(1, 3))

        self.seleniumDriver.find_element(By.NAME, 'commit').click()
        time.sleep(random.randint(1, 3))

        Wait(self.seleniumDriver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(),'" + config.CONTINUE_BUTTON_TEXT + "')]")))

    def isLoggedIn(self) -> bool:
        self.seleniumDriver.refresh()

        content = self.seleniumDriver.page_source
        content = str(content).lower()
        return content.find("too many requests") == -1 and content.find("need to sign in") == -1

    def loginIfNotBlocked(self) -> bool:
        try:
            self.seleniumDriver.get(config.BASE_URL)
            Wait(self.seleniumDriver, 60).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="header"]/nav/div[1]/div[2]')))

            self.login()

            return True
        except Exception as error:
            print(error)
            return False
