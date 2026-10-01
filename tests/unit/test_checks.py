from tester.checks import check_heartbeat_timeout, check_alive_counter, check_signal_range

def test_heartbeat_timeout():
    assert check_heartbeat_timeout(1.0, 1.1, 0.35) == True
    assert check_heartbeat_timeout(1.0, 1.5, 0.35) == False

def test_alive_counter():
    assert check_alive_counter(5, 6) == True
    assert check_alive_counter(15, 0) == True
    assert check_alive_counter(5, 5) == False
    assert check_alive_counter(5, 7) == False

def test_signal_range():
    assert check_signal_range(12.0, 11.0, 14.8) == True
    assert check_signal_range(10.0, 11.0, 14.8) == False
    assert check_signal_range(15.0, 11.0, 14.8) == False
