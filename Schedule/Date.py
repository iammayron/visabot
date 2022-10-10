from datetime import datetime

from Request import Request


class Date():
    def __init__(self) -> None:
        self.request = Request()

    def allAvailable(self, url: str, qty: int = 5) -> list or bool:
        dates = self.request.json(url)[:qty]
        if len(dates):
            self.printDates(dates)
            return dates
        else:
            return False

    def allFiltered(self, url: str, currentDate: str, fromDate: str or None = None, toDate: str or None = None, filterQty: int = 5) -> list:
        dates = self.allAvailable(url, filterQty)
        if dates is not False:
            return self.allFilteredDates(currentDate, dates, fromDate, toDate)
        else:
            return False

    def firstAvailable(self, url: str, currentDate: str, fromDate: str or None = None, toDate: str or None = None, filterQty: int = 5) -> str:
        dates = self.allAvailable(url, filterQty)
        filteredDates = self.allFilteredDates(
            currentDate, dates, fromDate, toDate)
        return filteredDates[0]

    def allFilteredDates(self, currentDate: str, dates: list, fromDate: str or None = None, toDate: str or None = None) -> str:
        lastDate = None
        availableDates: list = []

        for date in dates:
            date: dict = date
            date = date.get('date')
            if self.isEarlier(currentDate, date) and date != lastDate:
                if (fromDate != "null" and fromDate is not None) and (toDate != "null" and toDate is not None):
                    if self.isBetween(date, fromDate, toDate):
                        availableDates.append(date)
                else:
                    availableDates.append(date)
            lastDate = date

        return availableDates

    def isEarlier(self, oldDate: str, newDate: str) -> bool:
        return datetime.strptime(oldDate, '%Y-%m-%d') > datetime.strptime(newDate, '%Y-%m-%d')

    def isBetween(self, date: str, fromDate: str, toDate: str) -> bool:
        """
            Verifies if a date is between two dates.
            Arguments:
                date: a string with the date in format 'YYYY-MM-DD'
                fromDate: a string with the date in format 'YYYY-MM-DD'
                toDate: a string with the date in format 'YYYY-MM-DD'
        """
        date = datetime.strptime(date, '%Y-%m-%d')
        fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
        toDate = datetime.strptime(toDate, '%Y-%m-%d')
        return date >= fromDate and date <= toDate

    def printDates(self, dates: list):
        print()
        for date in dates:
            date: dict = date
            print("Available date: %s \t Business day: %s" %
                  (date.get('date'), date.get('business_day')))
        print()
