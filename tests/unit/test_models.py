import mailpit.client.models as models


def test_millis_one_digit():
    isoformat = "2009-06-30T18:30:00.2+02:00"
    isoformat_expected = "2009-06-30T18:30:00.200+02:00"
    isoformat_given = models.millis_to_3_digit(isoformat)
    assert isoformat_given == isoformat_expected


def test_millis_two_digits():
    isoformat = "2009-06-30T18:30:00.22+02:00"
    isoformat_expected = "2009-06-30T18:30:00.220+02:00"
    isoformat_given = models.millis_to_3_digit(isoformat)
    assert isoformat_given == isoformat_expected


def test_millis_zero():
    isoformat = "2009-06-30T18:30:00+02:00"
    isoformat_expected = "2009-06-30T18:30:00.000+02:00"
    isoformat_given = models.millis_to_3_digit(isoformat)
    assert isoformat_given == isoformat_expected
