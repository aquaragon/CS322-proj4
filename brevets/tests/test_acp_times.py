"""
Nose tests for apctimes

"""
from acp_times import open_time, close_time
import nose 
import logging
import arrow
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

time = arrow.get("2017-01-01T00:00:00+00:00").isoformat()

def test_zero_checkpoint():
    """
    Test to ensure it shifts by 1 hour.
    """
    close = arrow.get(close_time(0, 200, time))
    assert close.format("YYYY-MM-DD HH:mm") == "2017-01-01 01:00"
    test = arrow.get(open_time(0, 200, time))
    assert test.format("YYYY-MM-DD HH:mm") == "2017-01-01 00:00"

def test_standard():
    """
    Test standard inputs.
    """
    test_cases = [
        (60, "2017-01-01 04:00", "2017-01-01 01:46"),
        (120, "2017-01-01 08:00", "2017-01-01 03:32"),
        (175, "2017-01-01 11:40", "2017-01-01 05:09"),
        (205, "2017-01-01 13:30", "2017-01-01 05:53"),
    ]

    for control, close_time_str, open_time_str in test_cases:
        close = arrow.get(close_time(control, 200, time))
        assert close.format("YYYY-MM-DD HH:mm") == close_time_str
        test = arrow.get(open_time(control, 200, time))
        assert test.format("YYYY-MM-DD HH:mm") == open_time_str

def test_diffcontrol():
    close = arrow.get(close_time(200, 200, time))
    assert(close.format("YYYY-MM-DD HH:mm") == "2017-01-01 13:30")
    close = arrow.get(close_time(300, 300, time))
    assert(close.format("YYYY-MM-DD HH:mm") == "2017-01-01 20:00")
    close = arrow.get(close_time(400, 400, time))
    assert(close.format("YYYY-MM-DD HH:mm") == "2017-01-02 03:00")
    close = arrow.get(close_time(600, 600, time))
    assert(close.format("YYYY-MM-DD HH:mm") == "2017-01-02 16:00")
    close = arrow.get(close_time(1000, 1000, time))
    assert(close.format("YYYY-MM-DD HH:mm") == "2017-01-04 03:00")

def test_european():
    """
    Test for people in europe.
    """
    close = arrow.get(close_time(20, 200, time))
    assert close.format("YYYY-MM-DD HH:mm") == "2017-01-01 02:00"
    test = arrow.get(open_time(20, 200, time))
    assert test.format("YYYY-MM-DD HH:mm") == "2017-01-01 00:35"

def test_large():
    """
    Test for brevet speed time changes.
    """
    close_times = [
        (100, "2017-01-01 06:40"),
        (200, "2017-01-01 13:20"),
        (300, "2017-01-01 20:00"),
        (400, "2017-01-02 02:40"),
        (500, "2017-01-02 09:20"),
        (600, "2017-01-02 16:00"),
        (700, "2017-01-03 00:45"),
        (800, "2017-01-03 09:30"),
        (900, "2017-01-03 18:15"),
        (1000, "2017-01-04 03:00"),
    ]

    open_times = [
        (100, "2017-01-01 02:56"),
        (200, "2017-01-01 05:53"),
        (300, "2017-01-01 09:00"),
        (400, "2017-01-01 12:08"),
        (500, "2017-01-01 15:28"),
        (600, "2017-01-01 18:48"),
        (700, "2017-01-01 22:22"),
        (800, "2017-01-02 01:57"),
        (900, "2017-01-02 05:31"),
        (1000, "2017-01-02 09:05"),
    ]

    for control, close_time_str in close_times:
        close = arrow.get(close_time(control, 1000, time))
        assert close.format("YYYY-MM-DD HH:mm") == close_time_str

    for control, open_time_str in open_times:
        test = arrow.get(open_time(control, 1000, time))
        assert test.format("YYYY-MM-DD HH:mm") == open_time_str










