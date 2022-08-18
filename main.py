import time
from datetime import datetime

import config
from Auth import Auth
from Schedule import Date, Reschedule, Time

Auth = Auth()
Date = Date()
Time = Time()
Reschedule = Reschedule()

Auth.login()

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
                consulateDate = Date.firstAvailable(
                    config.CONSULATE_DATE_URL, config.CONSULATE_SCHEDULED_DATE, config.SCHEDULE_CONSULATE_DATE_FROM, config.SCHEDULE_CONSULATE_DATE_TO)

                if consulateDate:
                    print("Valid consulate date: %s" % consulateDate)
                    consulateTimeUrl = config.CONSULATE_TIME_URL % consulateDate
                    consulateTime = Time.firstAvailable(consulateTimeUrl)
                    if consulateTime:
                        print("Valid consulate time: %s" % consulateTime)
                        if config.CONSULATE_SCHEDULED_STATE not in config.NON_BIOMETRICS_STATE:
                            print("State requires a biometrics appointment")
                            biometricsDateUrl = config.BIOMETRICS_DATE_URL % (
                                consulateDate, consulateTime)
                            biometricsDate = Date.firstAvailable(
                                biometricsDateUrl, consulateDate)
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
                                        break
                        else:
                            if Reschedule.run(consulateDate, consulateTime):
                                break
            if(EXIT):
                break

            time.sleep(60 * 5)
        except:
            retry_count += 1
            time.sleep(60 * 5)
