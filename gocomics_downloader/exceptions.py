import mainchecker

mainchecker.check_for_main(__name__)


class ComicsException(Exception):
    """
    basic exception for all exceptions in this module.
    """

    def __init__(self):
        Exception.__init__(self, 'There was an error with downloading your comic.')


class InputException(ComicsException):
    """
    exception for inputs.
    """

    def __init__(self):
        Exception.__init__(self, 'There was a problem with your input. Please try again.')


class DoubleInputException(InputException):
    """
    both datetime and year/month/day was entered
    """

    def __init__(self, year, month, day, datetime):
        Exception.__init__(self, 'Both datetime and year/month/day was entered. Please remove one of them. Printing '
                                 'values: \nYear = {y} \nMonth = {m} \nDay = {d}\nDatetime = {dt}'.format(y=
                                                                                                          year, m=month,
                                                                                                          d=day,
                                                                                                          dt=datetime))


class NoInputException(InputException):
    """
    neither was given
    """

    def __init__(self):
        Exception.__init__(self, 'No input was given. Please either provide an datetime element or year/month/day.')


class IncompleteInputException(InputException):
    """
    incomplete
    """

    def __init__(self, year, month, day):
        Exception.__init__(self, 'The input is incomplete. Please make sure that the year, month and day variables '
                                 'have values. Printing values. \nYear = {y} \nMonth = {m} \nDay = {d}'.format(y=
                                                                                                               year,
                                                                                                               m=month,
                                                                                                               d=day))


class InvalidDate(ComicsException):
    """
    redirects, not valid comic date
    """

    def __init__(self, url):
        Exception.__init__(self, 'The date is invalid, and as a result will not work. Please choose an different date '
                                 'to download from. URL: {u}'.format(u=str(url)))
