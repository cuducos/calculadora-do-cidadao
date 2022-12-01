from datetime import date, datetime
from decimal import Decimal

from pytest import approx, mark, raises
from freezegun import freeze_time

from calculadora_do_cidadao import (
    AllUrbanCityAverage,
    CestaBasica,
    CestaBasicaAracaju,
    CestaBasicaBelem,
    CestaBasicaBeloHorizonte,
    CestaBasicaBoaVista,
    CestaBasicaBrasilia,
    CestaBasicaCampoGrande,
    CestaBasicaCentroOeste,
    CestaBasicaCuiaba,
    CestaBasicaCuritiba,
    CestaBasicaFlorianopolis,
    CestaBasicaFortaleza,
    CestaBasicaGoiania,
    CestaBasicaJoaoPessoa,
    CestaBasicaMacae,
    CestaBasicaMacapa,
    CestaBasicaMaceio,
    CestaBasicaManaus,
    CestaBasicaNatal,
    CestaBasicaNordeste,
    CestaBasicaNorte,
    CestaBasicaPalmas,
    CestaBasicaPortoAlegre,
    CestaBasicaPortoVelho,
    CestaBasicaRecife,
    CestaBasicaRioBranco,
    CestaBasicaRioDeJaneiro,
    CestaBasicaSalvador,
    CestaBasicaSaoLuis,
    CestaBasicaSaoPaulo,
    CestaBasicaSudeste,
    CestaBasicaSul,
    CestaBasicaTeresina,
    CestaBasicaVitoria,
    Igpm,
    Inpc,
    Ipca,
    Ipca15,
    IpcaE,
)
from calculadora_do_cidadao.adapters import AdapterDateNotAvailableError
from tests import fixture_generator


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
        (CestaBasica, date(2018, 7, 6), None, None, "1.460165126797113622157204568"),
        (CestaBasica, date(2014, 7, 8), 7, None, "12.73085672787343640166763121"),
        (
            CestaBasica,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "9.800127168524684637393180756",
        ),
        (
            CestaBasicaCentroOeste,
            date(2018, 7, 6),
            None,
            None,
            "1.523656211927287441557698990",
        ),
        (
            CestaBasicaCentroOeste,
            date(2014, 7, 8),
            7,
            None,
            "13.85141773482304019009756209",
        ),
        (
            CestaBasicaCentroOeste,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "9.898117261265336122575903207",
        ),
        (
            CestaBasicaNordeste,
            date(2018, 7, 6),
            None,
            None,
            "1.384965255233770727275985515",
        ),
        (
            CestaBasicaNordeste,
            date(2014, 7, 8),
            7,
            None,
            "12.24645904436860068259385665",
        ),
        (
            CestaBasicaNordeste,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "9.168529280286097451944568616",
        ),
        (
            CestaBasicaNorte,
            date(2018, 7, 6),
            None,
            None,
            "1.398587144692019880493661697",
        ),
        (CestaBasicaNorte, date(2014, 7, 8), 7, None, "11.03941941374641856364724033"),
        (
            CestaBasicaNorte,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "10.78471986417657045840407470",
        ),
        (
            CestaBasicaSudeste,
            date(2018, 7, 6),
            None,
            None,
            "1.486390590661870326945034438",
        ),
        (
            CestaBasicaSudeste,
            date(2014, 7, 8),
            7,
            None,
            "12.89231003270708146345173804",
        ),
        (
            CestaBasicaSudeste,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "10.32243712214399748750294433",
        ),
        (CestaBasicaSul, date(2018, 7, 6), None, None, "1.426849010558871143112571581"),
        (CestaBasicaSul, date(2014, 7, 8), 7, None, "12.57287547904373745361640002"),
        (
            CestaBasicaSul,
            date(1998, 7, 12),
            3,
            date(2014, 7, 8),
            "10.14474766867800329127811300",
        ),
        (
            CestaBasicaAracaju,
            date(2018, 7, 6),
            None,
            None,
            "1.313926179361535562063266549",
        ),
        (
            CestaBasicaBelem,
            date(2018, 7, 6),
            None,
            None,
            "1.387084267951593697211376035",
        ),
        (
            CestaBasicaBeloHorizonte,
            date(2018, 7, 6),
            None,
            None,
            "1.564991191367540189385597886",
        ),
        (
            CestaBasicaBoaVista,
            date(2015, 12, 1),
            1,
            date(2017, 8, 1),
            "1.037235504259411926353393790",
        ),
        (
            CestaBasicaBrasilia,
            date(2018, 7, 6),
            None,
            None,
            "1.516165394271660603576369319",
        ),
        (
            CestaBasicaCampoGrande,
            date(2018, 7, 6),
            None,
            None,
            "1.555573544887881486278636768",
        ),
        (
            CestaBasicaCuiaba,
            date(2018, 7, 6),
            None,
            None,
            "0.9927400046340395952938753443",
        ),
        (
            CestaBasicaCuritiba,
            date(2018, 7, 6),
            None,
            None,
            "1.380864765409383624655013799",
        ),
        (
            CestaBasicaFlorianopolis,
            date(2018, 7, 6),
            None,
            None,
            "1.482336792929901028246682881",
        ),
        (
            CestaBasicaFortaleza,
            date(2018, 7, 6),
            None,
            None,
            "1.410536307546274323682961557",
        ),
        (
            CestaBasicaGoiania,
            date(2018, 7, 6),
            None,
            None,
            "1.538839456302199901741361428",
        ),
        (
            CestaBasicaJoaoPessoa,
            date(2018, 7, 6),
            None,
            None,
            "1.368831917038744058764222958",
        ),
        (
            CestaBasicaMacae,
            date(2018, 7, 6),
            None,
            None,
            "1.573712797206672947957656708",
        ),
        (
            CestaBasicaMacapa,
            date(2015, 12, 1),
            1,
            date(2017, 8, 1),
            "1.052198847177926675834625625",
        ),
        (
            CestaBasicaMaceio,
            date(2015, 12, 1),
            1,
            date(2017, 8, 1),
            "1.155067192701269880409320676",
        ),
        (
            CestaBasicaManaus,
            date(2018, 7, 6),
            None,
            None,
            "1.014077765577047611003181575",
        ),
        (
            CestaBasicaNatal,
            date(2018, 7, 6),
            None,
            None,
            "1.345070216072004456301855815",
        ),
        (
            CestaBasicaPalmas,
            date(2015, 12, 1),
            1,
            date(2017, 7, 1),
            "1.067597248713947170683775504",
        ),
        (
            CestaBasicaPortoAlegre,
            date(2018, 7, 6),
            None,
            None,
            "1.415245276079260723644889890",
        ),
        (
            CestaBasicaPortoVelho,
            date(2015, 12, 1),
            None,
            date(2017, 8, 1),
            "1.084525282758223731545169367",
        ),
        (
            CestaBasicaRecife,
            date(2018, 7, 6),
            None,
            None,
            "1.351034740811098638574676913",
        ),
        (
            CestaBasicaRioBranco,
            date(2015, 12, 1),
            1,
            date(2017, 7, 1),
            "1.067854386416259325958322614",
        ),
        (
            CestaBasicaRioDeJaneiro,
            date(2018, 7, 6),
            None,
            None,
            "1.472160989831472658749911114",
        ),
        (
            CestaBasicaSalvador,
            date(2018, 7, 6),
            None,
            None,
            "1.489583981095703003544555687",
        ),
        (
            CestaBasicaSaoLuis,
            date(2018, 7, 6),
            None,
            None,
            "1.258383580360590489203077196",
        ),
        (
            CestaBasicaSaoPaulo,
            date(2018, 7, 6),
            None,
            None,
            "1.443601115632572813314434639",
        ),
        (
            CestaBasicaTeresina,
            date(2015, 12, 1),
            1,
            date(2017, 7, 1),
            "1.113623795803137460345178847",
        ),
        (
            CestaBasicaVitoria,
            date(2018, 7, 6),
            None,
            None,
            "1.476957901729695150456413159",
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
    ),
)
def test_adapter_indexes(adapter, original, value, target, expected, mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = fixture_generator(
        adapter
    )
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
    ),
)
def test_adapter_out_of_range(adapter, length, start_date, end_date, mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = fixture_generator(
        adapter
    )
    instance = adapter()
    assert len(instance.data) == length
    future_date, msg = get_error_msg_for_future(start_date, end_date)
    with raises(AdapterDateNotAvailableError, match=msg):
        instance.adjust(future_date)


def test_adapter_missing_date_within_range(mocker):
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = fixture_generator(
        "cestabasica"
    )
    bsb = CestaBasicaBrasilia()
    msg = (
        "This adapter has data from 07/1994 to 12/2020, but not for 11/2019. "
        "Available dates are:\n    -.+"
    )
    with raises(AdapterDateNotAvailableError, match=msg):
        bsb.adjust(date(2019, 11, 1))


@freeze_time("2018-07-06 21:00:00", tz_offset=-3)
@mark.parametrize(
    "adapter,original,value,target",
    (
        (Ipca, date(2018, 7, 6), None, None),
        (Ipca, datetime(2018, 7, 6, 21, 00, 00), None, None),
        (Ipca, "2018-07-06T21:00:00", None, None),
        (Ipca, "2018-07-06 21:00:00", None, None),
        (Ipca, "2018-07-06", None, None),
        (Ipca, "06/07/2018", None, None),
        (Ipca, "2018-07", None, None),
        (Ipca, "Jul/2018", None, None),
        (Ipca, "Jul-2018", None, None),
        (Ipca, "Jul 2018", None, None),
        (Ipca, "07/2018", None, None),
        (Ipca, 1530925200, None, None),
        (Ipca, 1530925200.0, None, None),
    ),
)
def test_string_date_inputs(adapter, original, value, target, mocker):
    expected = approx(Decimal("1.051202206630561280035407253"))
    download = mocker.patch("calculadora_do_cidadao.adapters.Download")
    download.return_value.return_value.__enter__.return_value = fixture_generator(
        adapter
    )
    instance = adapter()
    assert instance.adjust(original, value, target) == expected


def test_diesse_post_processing():
    body = b'<?xml version="1.0" encoding="UTF-8" ?><html></html>'
    assert CestaBasica.post_processing(body) == b"<html></html>"
