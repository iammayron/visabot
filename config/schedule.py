from ._loadenv import *

SCHEDULE_ID = os.getenv("SCHEDULE_ID")
SCHEDULE_CONSULATE_DATE_FROM = str(os.getenv("SCHEDULE_CONSULATE_DATE_FROM"))
SCHEDULE_CONSULATE_DATE_TO = str(os.getenv("SCHEDULE_CONSULATE_DATE_TO"))
SCHEDULE_TIME_FROM = str(os.getenv("SCHEDULE_TIME_FROM"))
SCHEDULE_TIME_TO = str(os.getenv("SCHEDULE_TIME_TO"))

CONSULATE_SCHEDULED_DATE = os.getenv("CONSULATE_SCHEDULED_DATE")
CONSULATE_SCHEDULED_STATE = {
    "Brasília": "54",
    "Porto Alegre": "128",
    "Recife": "57",
    "Rio de Janeiro": "55",
    "São Paulo": "56"
}[os.getenv("CONSULATE_SCHEDULED_STATE")]

NON_BIOMETRICS_STATE = [
    128,  # Porto Alegre
    57  # Recife
]

BIOMETRICS_SCHEDULED_STATE = {
    "Brasília": "58",
    "Rio de Janeiro": "59",
    "São Paulo": "60"
}[os.getenv("BIOMETRICS_SCHEDULED_STATE")]
