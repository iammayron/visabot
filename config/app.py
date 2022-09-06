from ._loadenv import *

LANGUAGE = str(os.getenv("APP_LANGUAGE", "pt-br")).lower()
SLEEP_TIME = int(os.getenv("APP_SLEEP_TIME", 5))
CONTINUE_BUTTON_TEXT = {
    "pt-br": "Continuar",
    "en-br": "Continue",
}[LANGUAGE]

CONFIRM_BUTTON_TEXT = {
    "pt-br": "Confirmar",
    "en-br": "Confirm",
}[LANGUAGE]

SUCCESS_MESSAGE = {
    "pt-br": "agendou com êxito",
    "en-br": "successfully scheduled",
}[LANGUAGE]