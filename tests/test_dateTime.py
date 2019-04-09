from date_time import DateTime, DateRange


class TestDateTime:

    def test_greater_hour(self):
        assert DateTime(0, 0, 0) < DateTime(0, 1, 0)

    def test_greater_minute(self):
        assert DateTime(0, 0, 0) < DateTime(0, 0, 1)

    def test_less_hour(self):
        assert DateTime(0, 1, 0) > DateTime(0, 0, 0)

    def test_less_minute(self):
        assert DateTime(0, 0, 1) > DateTime(0, 0, 0)

    def test_not_greater_hour(self):
        assert not DateTime(0, 2, 0) < DateTime(0, 1, 0)

    def test_not_greater_minute(self):
        assert not DateTime(0, 0, 2) < DateTime(0, 0, 1)

    def test_greater_equal_hour(self):
        assert DateTime(0, 0, 0) <= DateTime(0, 1, 0)

    def test_greater_equal_minute(self):
        assert DateTime(0, 0, 0) <= DateTime(0, 0, 1)

    def test_not_greater_equal_hour(self):
        assert not DateTime(0, 2, 0) <= DateTime(0, 1, 0)

    def test_not_greater_equal_minute(self):
        assert not DateTime(0, 0, 2) <= DateTime(0, 0, 1)

    def test_equal(self):
        assert DateTime(0, 0, 0) == DateTime(0, 0, 0)

    def test_not_equal(self):
        assert DateTime(0, 0, 0) != DateTime(0, 1, 0)

    def test_equal_day(self):
        assert DateTime(1, 0, 0) == DateTime(1, 0, 0)

    def test_not_equal_day(self):
        assert DateTime(0, 0, 0) != DateTime(1, 0, 0)

    def test_greater_day(self):
        assert DateTime(0, 0, 0) < DateTime(1, 0, 0)

    def test_greater_equal_day(self):
        assert DateTime(0, 0, 0) <= DateTime(0, 0, 0)

    def test_not_greater_equal_day(self):
        assert not DateTime(1, 0, 0) <= DateTime(0, 0, 0)

    def test_not_greater_day(self):
        assert not DateTime(2, 0, 0) < DateTime(1, 0, 0)


class TestDateRange:

    def test_in_range(self):
        sut = DateRange(DateTime(0, 0, 0), DateTime(0, 2, 0))
        assert sut.in_range(DateTime(0, 1, 0))

    def test_not_in_range(self):
        sut = DateRange(DateTime(0, 0, 0), DateTime(0, 1, 0))
        assert not sut.in_range(DateTime(0, 2, 0))
