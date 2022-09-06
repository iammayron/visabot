import random
import time

import config
from Base import Base
from Notification import Notification
from Selenium import By, Select

Notification = Notification()


class Reschedule(Base):
    def __init__(self) -> None:
        super().__init__()
        self.consulateStateFieldId = 'appointments_consulate_appointment_facility_id'
        self.consulateDateFieldId = 'appointments_consulate_appointment_date'
        self.consulateTimeFieldId = 'appointments_consulate_appointment_time'
        self.biometricsStateFieldId = 'appointments_asc_appointment_facility_id'
        self.biometricsDateFieldId = 'appointments_asc_appointment_date'
        self.biometricsTimeFieldId = 'appointments_asc_appointment_time'

    def run(self, consulateDate: str, consulateTime: str, biometricsDate: str or None = None, biometricsTime: str or None = None) -> bool:
        self.goToSchedulePage()

        retryCount = 1
        while 1:
            if retryCount > 1:
                Notification.sendAll(
                    "Erro!", "Uma tentativa de reagendamento falhou!")

            if retryCount > 3:
                return False

            if self.handleConsulateSelection(consulateDate, consulateTime):
                if biometricsDate is not None and biometricsTime is not None:
                    if self.handleBiometricsSelection(biometricsDate, biometricsTime):
                        if self.handleConfirmation():
                            Notification.sendAll("Sucesso!", "Reagendamento realizado para: Consulado: %s - %s %s Biometria: %s - %s %s" % (
                                config.CONSULATE_SCHEDULED_STATE, consulateDate, consulateTime, config.BIOMETRICS_SCHEDULED_STATE, biometricsDate, biometricsTime))
                            return True
                else:
                    if self.handleConfirmation():
                        Notification.sendAll("Sucesso!", "Reagendamento realizado para: Consulado: %s - %s %s" % (
                            config.CONSULATE_SCHEDULED_STATE, consulateDate, consulateTime))
                        return True
            retryCount += 1

    def goToSchedulePage(self):
        self.seleniumDriver.get(config.APPOINTMENT_URL)

    def selectOption(self, fieldId: str, option: str, nextFieldId: str or None = None) -> bool:
        option = str(option)
        loop = True

        print("selecting: %s - %s", fieldId, option)
        while loop:
            try:
                field = Select(self.seleniumDriver.find_element(
                    By.ID, fieldId))

                if self.optionExist(field.options, option) is False:
                    print('option not found')
                    return False

                field.select_by_index(0)
                time.sleep(random.randint(1, 3))
                selection = field.select_by_value(option)
                print(selection)
                time.sleep(random.randint(1, 3))

                print(nextFieldId)
                if (nextFieldId is not None):
                    nextField = self.seleniumDriver.find_elements(
                        By.ID, nextFieldId)
                    print(len(nextField))
                    if len(nextField):
                        loop = False
                else:
                    loop = False

                return True
            except Exception as error:
                content = self.seleniumDriver.page_source
                if content.find('too many requests') != -1:
                    exit()
                print('Error from field %s: %s' % (fieldId, error))
                return False

    def optionExist(self, allOptions: list, option: str) -> bool:
        for _option in allOptions:
            value = _option.get_attribute('value')
            if value == option:
                return True
        return False

    def selectDate(self, fieldId: str, date: str) -> bool:
        print("selecting: %s - %s", fieldId, date)
        self.seleniumDriver.find_element(
            By.ID, fieldId).click()
        jsSelectDate = '$("#%s").datepicker("setDate", "%s")' % (
            fieldId, date)
        self.seleniumDriver.execute_script(jsSelectDate)
        time.sleep(random.randint(1, 3))

        try:
            _year, _month, _day = date.split("-")
            _month = int(_month) - 1
            _day = int(_day)

            dateSelector = '//td[@data-month="%s" and @data-year="%s"]//a[contains(text(),"%s")]' % (
                _month, _year, _day
            )

            print('find element')
            dateElement = self.seleniumDriver.find_element(
                By.XPATH, dateSelector)
            print('click')
            dateElement.click()
            print("date selected")
            time.sleep(random.randint(1, 3))

            return True
        except Exception as error:
            content = self.seleniumDriver.page_source
            if content.find('Too Many Requests') != -1:
                exit()
            print('error from field %s: %s' % (fieldId, error))
            return False

    def handleConsulateSelection(self, consulateDate: str, consulateTime: str) -> bool:
        selectConsulateState = self.selectOption(self.consulateStateFieldId,
                                                 config.CONSULATE_SCHEDULED_STATE, self.consulateDateFieldId)

        if selectConsulateState:
            selectConsulateDate = self.selectDate(
                self.consulateDateFieldId, consulateDate)
            print(selectConsulateDate)
            if selectConsulateDate:
                selectConsulateTime = self.selectOption(
                    self.consulateTimeFieldId, consulateTime)
                if selectConsulateTime:
                    return True
        return False

    def handleBiometricsSelection(self, biometricsDate: str, biometricsTime: str) -> bool:
        selectBiometricsState = self.selectOption(
            self.biometricsStateFieldId, config.BIOMETRICS_SCHEDULED_STATE, self.biometricsDateFieldId)

        if selectBiometricsState:
            selectBiometricsDate = self.selectDate(
                self.biometricsDateFieldId, biometricsDate)
            if selectBiometricsDate:
                selectBioemetricsTime = self.selectOption(
                    self.biometricsTimeFieldId, biometricsTime)
                if selectBioemetricsTime:
                    return True
        return False

    def handleConfirmation(self) -> bool:
        try:
            print('clicking on confirm button')
            self.seleniumDriver.find_element(By.NAME, 'commit').click()
            time.sleep(random.randint(1, 3))
            # return True

            print('clicking on confirm button 2')
            self.seleniumDriver.find_element(
                By.XPATH, '//a[contains(@class,"alert") and contains(text(),"%s")]' % config.CONFIRM_BUTTON_TEXT).click()
            time.sleep(random.randint(1, 3))

            content = self.seleniumDriver.page_source
            if (content.find(config.SUCCESS_MESSAGE) != -1):
                return True
            else:
                return False
        except:
            return False
