import time
from datetime import datetime

from playsound import playsound

import config
from Auth import Auth
from Schedule import Date, Reschedule, Time

Auth = Auth()
Date = Date()
Time = Time()
Reschedule = Reschedule()

Auth.login()


def notify():
    playsound('/Users/mayronalvesdearaujo/Downloads/notification.wav')
    playsound('/Users/mayronalvesdearaujo/Downloads/notification.wav')
    playsound('/Users/mayronalvesdearaujo/Downloads/notification.wav')


def customMessage(message: str) -> None:
    print()
    print(message)
    print()


if __name__ == "__main__":
    retry_count = 0
    EXIT = False
    while 1:
        if retry_count > 6:
            break
        try:
            print(datetime.today())
            print("------------------")
            print()
            if Auth.isLoggedIn() == True:
                consulateDates = Date.allFiltered(config.CONSULATE_DATE_URL, config.CONSULATE_SCHEDULED_DATE,
                                                  config.SCHEDULE_CONSULATE_DATE_FROM, config.SCHEDULE_CONSULATE_DATE_TO)

                if len(consulateDates):
                    notify()
                    rescheduleStatus = False
                    for consulateDate in consulateDates:
                        if rescheduleStatus is True:
                            break

                        print("Valid consulate date: %s" % consulateDate)

                        consulateTimeUrl = config.CONSULATE_TIME_URL % consulateDate
                        consulateTime = Time.firstAvailable(consulateTimeUrl)
                        if consulateTime:
                            print("Valid consulate time: %s" % consulateTime)
                            if config.CONSULATE_SCHEDULED_STATE not in config.NON_BIOMETRICS_STATE:
                                customMessage(
                                    "State requires a biometrics appointment")

                                biometricsDateUrl = config.BIOMETRICS_DATE_URL % (
                                    consulateDate, consulateTime)
                                biometricsDates = Date.allFiltered(
                                    biometricsDateUrl, consulateDate)
                                if len(biometricsDates):
                                    for biometricsDate in biometricsDates:
                                        if biometricsDate:
                                            print("Valid biometrics date: %s" %
                                                  biometricsDate)
                                            biometricsTimeUrl = config.BIOMETRICS_TIME_URL % (
                                                consulateDate, consulateTime, biometricsDate)
                                            biometricsTime = Time.firstAvailable(
                                                biometricsTimeUrl)
                                            if biometricsTime:
                                                print("Valid biometrics time: %s" %
                                                      biometricsTime)
                                                if Reschedule.run(
                                                        consulateDate, consulateTime, biometricsDate, biometricsTime):
                                                    rescheduleStatus = True
                                                    break
                                            else:
                                                customMessage(
                                                    "No available biometrics time on the specified biometrics date: %s" % biometricsDate)
                                else:
                                    customMessage(
                                        "No available biometrics date before the specified consulate date: %s" % consulateDate)
                            else:
                                if Reschedule.run(consulateDate, consulateTime):
                                    rescheduleStatus = True
                                    break
                        else:
                            customMessage(
                                "No available consulate time on the specified consulate date: %s" % consulateDate)

            if(EXIT):
                break

            time.sleep(60 * 5)
        except:
            retry_count += 1
            time.sleep(60 * 5)
