import json
import time
import argparse
from tester.decoder import DBCDecoder
from tester.checks import check_heartbeat_timeout, check_alive_counter, check_signal_range
from tester.bus import get_socketcan_bus

class TestRunner:
    def __init__(self, bus, dbc_path, config_path):
        self.bus = bus
        self.decoder = DBCDecoder(dbc_path)
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.last_status_time = None
        self.last_counter = None
        self.failures = []

    def run_checks(self, duration=5.0):
        start_time = time.time()
        timeout_s = self.config["heartbeat_timeout_ms"] / 1000.0
        
        while time.time() - start_time < duration:
            msg = self.bus.recv(timeout=0.1)
            now = time.time()
            
            if msg:
                decoded = self.decoder.decode(msg)
                if not decoded:
                    continue
                    
                if msg.arbitration_id == 0x100:
                    if not check_heartbeat_timeout(self.last_status_time, now, timeout_s):
                        self.failures.append("Heartbeat timeout exceeded")
                        
                    self.last_status_time = now
                    
                    counter = decoded["alive_counter"]
                    if not check_alive_counter(self.last_counter, counter, self.config["alive_counter_modulus"]):
                        self.failures.append(f"Bad alive counter sequence: {self.last_counter} -> {counter}")
                    self.last_counter = counter
                    
                elif msg.arbitration_id == 0x200:
                    batt = decoded["battery_voltage"]
                    batt_lim = self.config["battery_voltage"]
                    if not check_signal_range(batt, batt_lim["min"], batt_lim["max"]):
                        self.failures.append(f"Battery voltage {batt} out of range")
                        
                    temp = decoded["temperature"]
                    temp_lim = self.config["temperature"]
                    if not check_signal_range(temp, temp_lim["min"], temp_lim["max"]):
                        self.failures.append(f"Temperature {temp} out of range")
                        
            else:
                if self.last_status_time and now - self.last_status_time > timeout_s:
                    self.failures.append("Heartbeat timeout exceeded")
                    self.last_status_time = now
                    
        return {
            "status": "FAIL" if self.failures else "PASS",
            "failures": list(set(self.failures))
        }

if __name__ == "__main__":
    import os
    bus = get_socketcan_bus("vcan0")
    dbc = os.path.join(os.path.dirname(__file__), "..", "dbc", "demo_ecu.dbc")
    cfg = os.path.join(os.path.dirname(__file__), "..", "config", "test_limits.json")
    
    runner = TestRunner(bus, dbc, cfg)
    print("Running tester for 5 seconds...")
    res = runner.run_checks(5.0)
    print(json.dumps(res, indent=2))
