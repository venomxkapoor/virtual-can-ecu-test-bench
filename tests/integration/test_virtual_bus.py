import threading
import os
import time
from ecu.ecu_sim import ECUSimulator
from tester.runner import TestRunner
from tester.bus import get_virtual_bus

def run_scenario(scenario_name):
    bus1 = get_virtual_bus()
    bus2 = get_virtual_bus()
    
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    dbc = os.path.join(base_dir, "dbc", "demo_ecu.dbc")
    cfg = os.path.join(base_dir, "config", "test_limits.json")
    scen = os.path.join(base_dir, "scenarios", scenario_name)
    
    sim = ECUSimulator(bus1, dbc, scen)
    tester = TestRunner(bus2, dbc, cfg)
    
    t = threading.Thread(target=sim.run, args=(2.5,))
    t.start()
    
    res = tester.run_checks(2.5)
    t.join()
    
    return res

def test_healthy():
    res = run_scenario("healthy.json")
    assert res["status"] == "PASS"

def test_overtemperature():
    res = run_scenario("overtemperature.json")
    assert res["status"] == "FAIL"
    assert any("Temperature" in f for f in res["failures"])

def test_drop_heartbeat():
    res = run_scenario("drop_heartbeat.json")
    assert res["status"] == "FAIL"
    assert any("Heartbeat" in f for f in res["failures"])

def test_bad_counter():
    res = run_scenario("bad_counter.json")
    assert res["status"] == "FAIL"
    assert any("alive counter" in f for f in res["failures"])

def test_low_voltage():
    res = run_scenario("low_voltage.json")
    assert res["status"] == "FAIL"
    assert any("Battery voltage" in f for f in res["failures"])
