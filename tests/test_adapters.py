from datetime import date
from decimal import Decimal

from pytest import approx, mark, raises

from calculadora_do_cidadao import (
    AllUrbanCityAverage,
    Igpm,
    Inpc,
    Ipca,
    Ipca15,
    IpcaE,
    Selic,
)
from calculadora_do_cidadao.adapters import AdapterDateNotAvailableError
from tests import get_fixture


def get_error_msg_for_future(start_date, end_date):
    try:
        future_date = end_date.replace(month=end_date.month + 1)
    except ValueError:
        future_date = end_date.replace(year=end_date.year + 1, month=1)

    data = {
        "start": start_date.strftime("%m/%Y"),
        "end": end_date.strftime("%m/%Y"),
        "future": future_date.strftime("%m/%Y"),
    }
    msg = r"This adapter has data from {start} to {end}\. {future} is out of range\."
    return future_date, msg.format(**data)


@mark.parametrize(
    "adapter,original,value,target,expected",
    (
        (
            AllUrbanCityAverage,
            date(2000, 1, 1),
            None,
            None,
            "1.526881275841701122268163024",
        ),
        (
            AllUrbanCityAverage,
            date(2019, 1, 1),
            42,
            None,
            "42.96874616599320069813553488",
        ),
        (
            AllUrbanCityAverage,
            date(2019, 1, 1),
            3,
            date(2006, 7, 1),
            "2.409042517403917316056721534",
        ),
        (Igpm, date(2018, 7, 6), None, None, "1.089562719284143684871778501"),
        (Igpm, date(2014, 7, 8), 7, None, "9.695966517693585432732393804"),
        (Igpm, date(1998, 7, 12), 3, date(2006, 7, 1), "6.880958439252658773596604453"),
        (Inpc, date(2014, 3, 6), None, None, "1.361007124894175467688242800"),
        (Inpc, date(2011, 5, 8), 9, None, "14.373499236614377437778943450"),
        (Inpc, date(2009, 1, 12), 5, date(2013, 8, 1), "6.410734265150376567640231785"),
        (Ipca, date(2018, 7, 6), None, None, "1.051202206630561280035407253"),
        (Ipca, date(2014, 7, 8), 7, None, "9.407523138792336916983267321"),
        (Ipca, date(1998, 7, 12), 3, date(2006, 7, 1), "5.279855889296777979447848574"),
        (Ipca15, date(2017, 2, 13), None, None, "1.101569276203612423894969769"),
        (Ipca15, date(2012, 5, 8), 3, None, "4.577960384607494629737626417"),
        (Ipca15, date(1999, 11, 10), 5, date(2002, 9, 5), "6.068815714507691510850986"),
        (IpcaE, date(2017, 2, 13), None, None, "1.101569276203612423894969769"),
        (IpcaE, date(2012, 5, 8), 3, None, "4.577960384607494629737626417"),
        (IpcaE, date(1999, 11, 10), 5, date(2002, 9, 5), "6.0688157145076915108509866"),
        (Selic, date(2019, 11, 1), None, None, "1.0037"),
        (Selic, date(2019, 10, 1), 3, None, "3.02254218"),
        (
            Selic,
            date(2019, 9, 1),
            5,
            date(2002, 9, 5),
            "0.6946147832098614982148570275",
        ),
    ),
)
def test_adapter_indexes(adapter, original, value, target, expected, mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = get_fixture(adapter)
    instance = adapter()
    assert instance.adjust(original, value, target) == approx(Decimal(expected))


@mark.parametrize(
    "adapter,length,start_date,end_date",
    (
        (AllUrbanCityAverage, 876, date(1947, 1, 1), date(2019, 12, 1)),
        (Igpm, 367, date(1989, 6, 1), date(2019, 12, 1)),
        (Inpc, 312, date(1994, 1, 1), date(2019, 12, 1)),
        (Ipca, 312, date(1994, 1, 1), date(2019, 12, 1)),
        (Ipca15, 312, date(1994, 1, 1), date(2019, 12, 1)),
        (IpcaE, 312, date(1994, 1, 1), date(2019, 12, 1)),
        (Selic, 300, date(1995, 1, 1), date(2019, 12, 1)),
    ),
)
def test_adapter_range(adapter, length, start_date, end_date, mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = get_fixture(adapter)
    instance = adapter()
    assert len(instance.data) == length
    future_date, msg = get_error_msg_for_future(start_date, end_date)
    with raises(AdapterDateNotAvailableError, match=msg):
        instance.adjust(future_date)
