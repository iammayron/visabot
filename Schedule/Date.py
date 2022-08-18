from datetime import datetime

from Request import Request


class Date():
    def __init__(self) -> None:
        self.request = Request()

    def allAvailable(self, url: str, qty: int = 5) -> list:
        dates = self.request.json(url)[:qty]
        self.printDates(dates)
        return dates

    def firstAvailable(self, url: str, currentDate: str, fromDate: str or None = None, toDate: str or None = None, filterQty: int = 5) -> str:
        dates = self.allAvailable(url, filterQty)
        return self.earliest(currentDate, dates, fromDate, toDate)

    def earliest(self, currentDate: str, dates: list, fromDate: str or None = None, toDate: str or None = None) -> str:
        lastDate = None
        for date in dates:
            date: dict = date
            date = date.get('date')
            print('is earlier', date, self.isEarlier(
                currentDate, date), lastDate)
            if self.isEarlier(currentDate, date) and date != lastDate:
                print('from to dates', fromDate, toDate)
                if fromDate != "null" and toDate != "null":
                    print('is between')
                    if self.isBetween(date, fromDate, toDate):
                        return date
                else:
                    return date
            lastDate = date
        print()

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
        for date in dates:
            date: dict = date
            print("%s \t business_day: %s" %
                  (date.get('date'), date.get('business_day')))
        print()
