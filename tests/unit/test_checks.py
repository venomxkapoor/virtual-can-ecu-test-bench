import pytest
from tester.checks import check_heartbeat_timeout, check_cycle_time, check_alive_counter, check_signal_range

def test_heartbeat_timeout():
    assert check_heartbeat_timeout(1.0, 1.1, 0.35) == True
    assert check_heartbeat_timeout(1.0, 1.5, 0.35) == False

def test_cycle_time():
    assert check_cycle_time(1.0, 1.1, 0.1, 0.04) == True
    assert check_cycle_time(1.0, 1.15, 0.1, 0.04) == False
    assert check_cycle_time(1.0, 1.05, 0.1, 0.04) == True

def test_alive_counter():
    assert check_alive_counter(5, 6) == True
    assert check_alive_counter(15, 0) == True
    assert check_alive_counter(5, 5) == False
    assert check_alive_counter(5, 7) == False

@pytest.mark.parametrize("value, expected", [
    (10.99, False),
    (11.00, True),
    (11.01, True),
    (14.79, True),
    (14.80, True),
    (14.81, False)
])
def test_signal_range_voltage(value, expected):
    assert check_signal_range(value, 11.0, 14.8) == expected

@pytest.mark.parametrize("value, expected", [
    (-20.01, False),
    (-20.00, True),
    (-19.99, True),
    (99.99, True),
    (100.00, True),
    (100.01, False)
])
def test_signal_range_temperature(value, expected):
    assert check_signal_range(value, -20.0, 100.0) == expected
