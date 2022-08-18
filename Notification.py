import os

import requests

import config


class Notification():
    def send(self, title, message, channel):
        if channel == 'macos':
            self.toMacOs(title, message)
        elif channel == 'push-notification' and config.PUSHOVER_ENABLED:
            self.toPushNotification(title, message)
        else:
            print("Unknown channel: %s" % channel)

    def sendAll(self, title, message):
        self.send(title, message, 'macos')
        self.send(title, message, 'push-notification')

    def toMacOs(self, title, message):
        systemCommand = """osascript -e 'display notification "{}" with title "{}"'"""
        os.system(systemCommand.format(message, title))

    def toPushNotification(self, title, message):
        requests.post(config.PUSHOVER_URL, {
            "user": config.PUSHOVER_USER,
            "token": config.PUSHOVER_TOKEN,
            "title": title,
            "message": message
        })
