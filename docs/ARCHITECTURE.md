# Architecture

## Components

- **ECU Simulator**: A Python class simulating a CAN node. Publishes `ECU_STATUS` and `SENSOR_DATA`.
- **vcan0**: Linux virtual CAN bus used for local demo. 
- **Test Runner**: Automates DBC decoding and limit checks.
- **pytest / CI**: Uses `python-can` virtual bus backend to run all scenarios safely on GitHub Actions without needing Linux kernel privileges.

## Data Flow
`ecu_sim.py` -> python-can -> `runner.py`
