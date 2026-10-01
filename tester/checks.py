def check_heartbeat_timeout(last_time, current_time, timeout_s):
    if last_time is None:
        return True
    return (current_time - last_time) <= timeout_s

def check_cycle_time(last_time, current_time, expected_period_s, tolerance_s):
    if last_time is None:
        return True
    delta = current_time - last_time
    return (expected_period_s - tolerance_s) <= delta <= (expected_period_s + tolerance_s)

def check_alive_counter(last_counter, current_counter, modulus=16):
    if last_counter is None:
        return True
    expected = (last_counter + 1) % modulus
    return current_counter == expected

def check_signal_range(value, min_val, max_val):
    return min_val <= value <= max_val
