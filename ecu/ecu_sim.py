import time
import json
import can
import cantools
import os
import argparse

class ECUSimulator:
    def __init__(self, bus, dbc_path, scenario_path=None):
        self.bus = bus
        self.db = cantools.database.load_file(dbc_path)
        self.state = "RUN"
        self.alive_counter = 0
        self.battery_voltage = 12.5
        self.temperature = 25.0
        
        self.scenario = {
            "name": "healthy",
            "overtemperature_at_sec": None,
            "drop_heartbeat_at_sec": None,
            "bad_counter_at_sec": None,
            "low_voltage_at_sec": None,
            "wrong_state": False
        }
        
        if scenario_path and os.path.exists(scenario_path):
            with open(scenario_path, "r") as f:
                self.scenario.update(json.load(f))
                
        self.start_time = time.time()
        self.last_status_time = 0
        self.last_sensor_time = 0
        
        self.status_period = 0.1
        self.sensor_period = 0.2

    def run(self, duration=None):
        print(f"Starting ECU Simulator (Scenario: {self.scenario.get('name', 'unknown')})")
        while True:
            now = time.time()
            elapsed = now - self.start_time
            
            if duration and elapsed > duration:
                break
                
            # Fault injection logic
            if self.scenario.get("overtemperature_at_sec") and elapsed >= self.scenario["overtemperature_at_sec"]:
                self.temperature = 110.0
                if not self.scenario.get("wrong_state"):
                    self.state = "FAULT"
                
            if self.scenario.get("low_voltage_at_sec") and elapsed >= self.scenario["low_voltage_at_sec"]:
                self.battery_voltage = 9.0
                
            if self.scenario.get("bad_counter_at_sec") and elapsed >= self.scenario["bad_counter_at_sec"]:
                self.alive_counter = (self.alive_counter + 2) % 16
                self.scenario["bad_counter_at_sec"] = None # Inject once
                
            drop_heartbeat = False
            if self.scenario.get("drop_heartbeat_at_sec"):
                if self.scenario["drop_heartbeat_at_sec"] <= elapsed <= self.scenario["drop_heartbeat_at_sec"] + 1.0:
                    drop_heartbeat = True

            # Send status message (100 ms)
            if now - self.last_status_time >= self.status_period:
                if not drop_heartbeat:
                    msg_data = self.db.encode_message("ECU_STATUS", {
                        "state": self.state,
                        "alive_counter": self.alive_counter
                    })
                    msg = can.Message(arbitration_id=0x100, data=msg_data, is_extended_id=False)
                    self.bus.send(msg)
                    self.alive_counter = (self.alive_counter + 1) % 16
                self.last_status_time = now

            # Send sensor message (200 ms)
            if now - self.last_sensor_time >= self.sensor_period:
                msg_data = self.db.encode_message("SENSOR_DATA", {
                    "battery_voltage": self.battery_voltage,
                    "temperature": self.temperature
                })
                msg = can.Message(arbitration_id=0x200, data=msg_data, is_extended_id=False)
                self.bus.send(msg)
                self.last_sensor_time = now
                
            time.sleep(0.01)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default=None, help="Path to scenario JSON")
    args = parser.parse_args()
    
    bus = can.Bus(channel="vcan0", interface="socketcan")
    dbc = os.path.join(os.path.dirname(__file__), "..", "dbc", "demo_ecu.dbc")
    sim = ECUSimulator(bus, dbc, args.scenario)
    try:
        sim.run()
    except KeyboardInterrupt:
        print("Stopped ECU simulator")
