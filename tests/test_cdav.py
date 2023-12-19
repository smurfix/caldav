import datetime

import tzlocal
from caldav.elements.cdav import _to_utc_date_string
from caldav.elements.cdav import CalendarQuery

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

SOMEWHERE_REMOTE = zoneinfo.ZoneInfo("Brazil/DeNoronha")  # UTC-2 and no DST


def test_element():
    cq = CalendarQuery()
    assert str(cq).startswith("<?xml")
    assert not "xml" in repr(cq)
    assert "CalendarQuery" in repr(cq)
    assert "calendar-query" in str(cq)


def test_to_utc_date_string_date():
    input = datetime.date(2019, 5, 14)
    res = _to_utc_date_string(input)
    assert res == "20190514T000000Z"


def test_to_utc_date_string_utc():
    input = datetime.datetime(2019, 5, 14, 21, 10, 23, 23, tzinfo=datetime.timezone.utc)
    try:
        res = _to_utc_date_string(input.astimezone())
    except:
        ## old python does not support astimezone() without a parameter given
        res = _to_utc_date_string(input.astimezone(tzlocal.get_localzone()))
    assert res == "20190514T211023Z"


def test_to_utc_date_string_dt_with_zoneinfo_tzinfo():
    input = datetime.datetime(2019, 5, 14, 21, 10, 23, 23, tzinfo=SOMEWHERE_REMOTE)
    res = _to_utc_date_string(input)
    assert res == "20190514T231023Z"


def test_to_utc_date_string_dt_with_local_tz():
    input = datetime.datetime(2019, 5, 14, 21, 10, 23, 23)
    try:
        res = _to_utc_date_string(input.astimezone())
    except:
        res = _to_utc_date_string(tzlocal.get_localzone())
    exp_dt = datetime.datetime(
        2019, 5, 14, 21, 10, 23, 23, tzinfo=tzlocal.get_localzone()
    ).astimezone(datetime.timezone.utc)
    exp = exp_dt.strftime("%Y%m%dT%H%M%SZ")
    assert res == exp


def test_to_utc_date_string_naive_dt():
    input = datetime.datetime(2019, 5, 14, 21, 10, 23, 23)
    res = _to_utc_date_string(input)
    exp_dt = datetime.datetime(
        2019, 5, 14, 21, 10, 23, 23, tzinfo=tzlocal.get_localzone()
    ).astimezone(datetime.timezone.utc)
    exp = exp_dt.strftime("%Y%m%dT%H%M%SZ")
    assert res == exp


class TestErrorUnitTestBot:
    # This test has been generated by UnitTestBot (utbot.org)

    def test_to_utc_date_string_with_exception(self):
        """
        ts = datetime.datetime(1, 1, 1)
        """
        # This test fails because function [caldav.elements.cdav._to_utc_date_string] produces [OverflowError]
        _to_utc_date_string(datetime.datetime(1, 1, 1))


class TestRegressionUnitTestBot:
    def test_to_utc_date_string_min(self):
        input_datetime = datetime.datetime(1, 1, 1)
        res = _to_utc_date_string(input_datetime)
        exp_dt = datetime.datetime(1, 1, 1, tzinfo=datetime.timezone.utc)
        exp = exp_dt.strftime("%Y%m%dT%H%M%SZ")
        assert res == exp
