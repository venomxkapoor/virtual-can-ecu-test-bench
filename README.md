# Virtual CAN ECU Test Bench

I do not have a physical CAN adapter or ECU, so this project simulates an ECU over Linux virtual CAN and validates its messages with pytest.

**Limitation Statement:**
No physical ECU, CAN adapter, CANoe, dSPACE or real vehicle network was used.

## Architecture
```text
+-----------------+
|  ECU Simulator  |
+--------+--------+
         | CAN frames
         v
+-----------------+
| SocketCAN/vcan0 |
+--------+--------+
         |
         v
+-----------------+
|   DBC Decoder   |
+--------+--------+
         |
         v
+-----------------+
| ValidationRunner|
+--------+--------+
         |
         v
+-----------------+
|   pytest / CI   |
+-----------------+
```

## Message table
| Message | Example ID | Period | Signals | Purpose |
| --- | --- | --- | --- | --- |
| ECU_STATUS | 0x100 | 100 ms | state, alive_counter | Shows that the ECU is alive and reports its operating state. |
| SENSOR_DATA | 0x200 | 200 ms | battery_voltage, temperature | Carries two values that the tester can validate. |

## How to install
```bash
pip install -r requirements.txt
```

## How to run the CI-safe virtual demo
```bash
pytest tests/
```

## How to run the local vcan0 demo
(Requires Linux/WSL2 with vcan support. `can-utils` provides command-line tools such as candump.)
```bash
sudo apt install can-utils
```

Terminal 1:
```bash
./scripts/setup_vcan.sh
```
Terminal 2:
```bash
candump vcan0
```
Terminal 3:
```bash
python -m ecu.ecu_sim
```
Terminal 4:
```bash
python -m tester.runner
```

**Example Output (Terminal 4):**
```json
{
  "status": "PASS",
  "failures": []
}
```

## Fault scenarios and expected output
- `healthy`: Status and sensor frames arrive on time; values remain inside limits; counter increments (PASS)
- `overtemperature`: Temperature rises above the configured limit; ECU state becomes FAULT (Tester detects high temperature and validates FAULT state)
- `overtemperature_wrong_state`: Temperature rises but state stays RUN (Tester catches invalid ECU behaviour)
- `drop-heartbeat`: ECU_STATUS stops for longer than the timeout (Heartbeat test FAILS)
- `bad-counter`: alive_counter repeats or skips unexpectedly (Counter sequence test FAILS)
- `low-voltage`: Battery voltage falls below minimum (Signal-range test FAILS)

## Automated tests
Tests verify DBC encoding/decoding, timing checks, and full end-to-end simulation using pytest and a virtual `python-can` backend. Boundary-value tests use pytest parametrization for voltage, temperature and timing limits.
