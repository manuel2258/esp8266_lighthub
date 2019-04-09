class DateTime:
    """
    A class to manage times and perform calculations on them
    """

    def __init__(self, day, hour, minute):
        """
        Initializes the object with a hour and minute value
        :param hour: Integer
        :param minute: Integer
        """
        self._day = int(day)
        self._hour = int(hour)
        self._minute = int(minute)

    def __eq__(self, other):
        """
        Compares if self and other are equal
        :param other: Other DateTime
        :return: True if equal, otherwise False
        """
        other_time = other.get_time()
        if self._day != other_time[0]:
            return False
        if self._hour == other_time[1] and self._minute == other_time[2]:
            return True
        return False

    def __lt__(self, other):
        """
        Compares if self is less then other
        :param other: Other DateTime
        :return: True if less, otherwise False
        """
        other_time = other.get_time()
        if self._day < other_time[0]:
            return True
        if self._hour < other_time[1]:
            return True
        elif self._minute < other_time[2]:
            return True
        return False

    def __le__(self, other):
        """
        Compares if self is less or equal then other
        :param other: Other DateTime
        :return: True if less or equal, otherwise False
        """
        other_time = other.get_time()
        if self._day > other_time[0]:
            return False
        if self._hour > other_time[1]:
            return False
        elif self._minute > other_time[2]:
            return False
        return True

    def __str__(self):
        """
        Returns the string representation of the object
        :return:
        """
        return "DateTime[{}, {}, {}]".format(self._day, self._hour, self._minute)

    def get_time(self):
        """
        Returns a tuple of (hour, minute) that the DateTime does represent
        :return:
        """
        return self._day, self._hour, self._minute


class DateRange:
    """
    A DateRange given by two DateTime objects
    """

    def __init__(self, start, end):
        """
        Creates a new DateRange object that represents the range between start and end
        :param start: Start DateTime object
        :param end: End StateTime object
        :exception assertionError: throws AssertionError if start >= end
        """
        assert start < end
        self._start = start
        self._end = end

    def in_range(self, datetime):
        """
        Checks if the given DateTime is in the range defined by the object
        :param datetime: The to check DateTime
        :return: True if in range, False otherwise
        """
        return self._start <= datetime <= self._end

    def __str__(self):
        """
        Returns the string representation of the object
        :return:
        """
        return "DateRange[{}, {}]".format(self._start, self._end)
