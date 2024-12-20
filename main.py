import time
from datetime import datetime

from playsound import playsound

import config
from Auth import Auth
from Notification import Notification
from Schedule import Date, Reschedule, Time
from Selenium import Selenium

Auth = Auth()
Notification = Notification()
Date = Date()
Time = Time()
Reschedule = Reschedule()

Auth.login()


def notify():
    playsound('./message-notification-103496.mp3')
    playsound('./message-notification-103496.mp3')
    playsound('./message-notification-103496.mp3')


def customMessage(message: str) -> None:
    print()
    print(message)
    print()


if __name__ == "__main__":
    RETRY_COUNT = 0
    EXIT = False
    START_TIME = datetime.today()
    END_TIME = None
    while 1:
        if RETRY_COUNT > 6:
            if (END_TIME == None):
                END_TIME = datetime.today()
                duration = END_TIME - START_TIME
                with open('duration.log', 'a') as f:
                    f.write('\nStarted at: %s' % START_TIME)
                    f.write('\nEnded at: %s' % END_TIME)
                    f.write('\nTime running: %s' % duration)
                    f.write('\nSleep time: %s minute(s)' % config.SLEEP_TIME)
                    f.write('\n------------------\n')
            Selenium.kill()
            RETRY_COUNT = 3
            time.sleep(60 * 60)
        try:
            print(datetime.today())
            print("------------------")
            consulateDates = Date.allFiltered(config.CONSULATE_DATE_URL, config.CONSULATE_SCHEDULED_DATE,
                                              config.SCHEDULE_CONSULATE_DATE_FROM, config.SCHEDULE_CONSULATE_DATE_TO)

            if Auth.isLoggedIn() == True:
                if consulateDates is not False:
                    if (END_TIME != None):
                        START_TIME = datetime.today()
                        duration = START_TIME - END_TIME
                        with open('duration.log', 'a') as f:
                            f.write('\nEnded at: %s' % END_TIME)
                            f.write('\nReturned at: %s' % START_TIME)
                            f.write('\nTime waiting: %s' % duration)
                            f.write('\n------------------\n')
                        END_TIME = None
                        RETRY_COUNT = 0
                    if len(consulateDates):
                        notify()
                        Notification.send(
                            'Consulate dates found!', 'We found some possible consulate dates.', 'push-notification')
                        rescheduleStatus = False
                        for consulateDate in consulateDates:
                            if rescheduleStatus is True:
                                break

                            print("Valid consulate date: %s" % consulateDate)

                            consulateTimeUrl = config.CONSULATE_TIME_URL % consulateDate
                            consulateTime = Time.firstAvailable(
                                consulateTimeUrl)
                            if consulateTime:
                                print("Valid consulate time: %s" %
                                      consulateTime)
                                if config.CONSULATE_SCHEDULED_STATE not in config.NON_BIOMETRICS_STATE:
                                    customMessage(
                                        "State requires a biometrics appointment")

                                    biometricsDateUrl = config.BIOMETRICS_DATE_URL % (
                                        consulateDate, consulateTime)
                                    biometricsDates = Date.allFiltered(
                                        biometricsDateUrl, consulateDate)
                                    if biometricsDates is not False:
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
                                                            EXIT = True
                                                            break
                                                    else:
                                                        customMessage(
                                                            "No available biometrics time on the specified biometrics date: %s" % biometricsDate)
                                        else:
                                            customMessage(
                                                "No available biometrics date before the specified consulate date: %s" % consulateDate)
                                    else:
                                        customMessage(
                                            "No data returned from biometrics date request")
                                else:
                                    if Reschedule.run(consulateDate, consulateTime):
                                        rescheduleStatus = True
                                        EXIT = True
                                        break
                            else:
                                customMessage(
                                    "No available consulate time on the specified consulate date: %s" % consulateDate)
                else:
                    customMessage(
                        "No data returned from consulate date request")
                    RETRY_COUNT += 1

                if EXIT:
                    break

                time.sleep(60 * config.SLEEP_TIME)
            else:
                Auth.login()
        except Exception as e:
            print(f"An error occurred: {e}")

            RETRY_COUNT += 1
            time.sleep(60 * config.SLEEP_TIME)
