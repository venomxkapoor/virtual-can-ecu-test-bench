# Virtual CAN ECU Test Bench

Virtual CAN ECU Test Bench | Python, SocketCAN, python-can, cantools, pytest
- Built a software-simulated ECU and automated validation bench over Linux virtual CAN, using a DBC to encode and decode status and sensor signals.
- Implemented pytest checks for heartbeat timing, alive-counter sequencing, signal limits and injected fault scenarios, with CI-safe virtual-bus tests.

**Limitation Statement:**
The project uses a software-simulated ECU and virtual CAN interfaces. No physical ECU, CAN adapter, CANoe, dSPACE or real vehicle network was used.

## What the project simulates
This project simulates a small vehicle ECU sending heartbeat (ECU_STATUS) and sensor data (SENSOR_DATA) over a Controller Area Network (CAN). An automated tester script validates the data.

## Concepts
- **CAN**: A robust communication protocol used in vehicles.
- **SocketCAN**: The Linux kernel networking stack for CAN.
- **DBC**: A file that describes how to unpack raw CAN bytes into meaningful data (like temperature).

## Architecture diagram
Please see `docs/ARCHITECTURE.md`.

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
(Requires Linux/WSL2 with vcan support)
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

## Fault scenarios and expected output
- `healthy`: Status and sensor frames arrive on time; values remain inside limits; counter increments (PASS)
- `overtemperature`: Temperature rises above the configured limit; ECU state becomes FAULT (Tester detects high temperature and validates FAULT state)
- `drop-heartbeat`: ECU_STATUS stops for longer than the timeout (Heartbeat test FAILS)
- `bad-counter`: alive_counter repeats or skips unexpectedly (Counter sequence test FAILS)
- `low-voltage`: Battery voltage falls below minimum (Signal-range test FAILS)

## Automated tests
Tests verify DBC encoding/decoding, timing checks, and full end-to-end simulation using pytest and a virtual `python-can` backend.

## Limitations
No physical hardware is used.

## What I learned
See `docs/LEARNING_MAP.md`.

## Future improvements
In the future, this test bench could be connected to a real USB-to-CAN adapter and used to validate a physical ECU written in C++.
