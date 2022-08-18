from ._loadenv import *

LANGUAGE = str(os.getenv("LANGUAGE", "pt-br")).lower()
CONTINUE_BUTTON_TEXT = {
    "pt-br": "Continuar",
    "en-br": "Continue",
}[LANGUAGE]

CONFIRM_BUTTON_TEXT = {
    "pt-br": "Confirmar",
    "en-br": "Confirm",
}[LANGUAGE]
