from .app import *
from .schedule import *

# Selenium Config
HUB_ADDRESS = "http://localhost:4444/wd/hub"

# AIS US Visa URLs / Textos
BASE_URL = "https://ais.usvisa-info.com/%s/niv" % LANGUAGE
SCHEDULE_URL = "%s/schedule/%s" % (BASE_URL, SCHEDULE_ID)
CONSULATE_DATE_URL = "%s/appointment/days/%s.json?appointments[expedite]=false" % (
    SCHEDULE_URL, CONSULATE_SCHEDULED_STATE
)
CONSULATE_TIME_URL = "%s/appointment/times/%s.json?date=%%s&appointments[expedite]=false" % (
    SCHEDULE_URL, CONSULATE_SCHEDULED_STATE
)
BIOMETRICS_DATE_URL = "%s/appointment/days/%s.json?consulate_id=%s&consulate_date=%%s&consulate_time=%%s&appointments[expedite]=false" % (
    SCHEDULE_URL, BIOMETRICS_SCHEDULED_STATE, CONSULATE_SCHEDULED_STATE
)
BIOMETRICS_TIME_URL = "%s/appointment/times/%s.json?consulate_id=%s&consulate_date=%%s&consulate_time=%%s&date=%%s&appointments[expedite]=false" % (
    SCHEDULE_URL, BIOMETRICS_SCHEDULED_STATE, CONSULATE_SCHEDULED_STATE
)
APPOINTMENT_URL = "%s/appointment" % SCHEDULE_URL
