from datetime import datetime

import config
from Request import Request


class Time():
    def __init__(self) -> None:
        self.request = Request()

    def allAvailable(self, url: str, qty: int = 5) -> list:
        return self.request.json(url)[:qty]

    def firstAvailable(self, url: str, filterQty: int = 5) -> str:
        slots = self.allAvailable(url, filterQty)
        return self.filterTime(slots)

    def filterTime(self, slots: list) -> str:
        fromSlot: str = config.SCHEDULE_TIME_FROM
        toSlot: str = config.SCHEDULE_TIME_TO

        for slot in slots:
            slot: dict = slot
            slot = slot.get('slot')
            if fromSlot and toSlot:
                if self.isBetween(slot, fromSlot, toSlot):
                    return slot
            else:
                return slot

    def isBetween(self, slot: str, fromSlot: str, toSlot: str) -> bool:
        """
            Verifies if a time slot is between two time slots.
            Arguments:
                slot: a string with the slot in format 'HH:MM'
                fromSlot: a string with the slot in format 'HH:MM'
                toSlot: a string with the slot in format 'HH:MM'
        """
        slot = datetime.strptime(slot, '%H-%M')
        fromSlot = datetime.strptime(fromSlot, '%H-%M')
        toSlot = datetime.strptime(toSlot, '%H-%M')
        return slot >= fromSlot and slot <= toSlot
