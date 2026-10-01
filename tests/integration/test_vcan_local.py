import pytest
import os
import can

@pytest.mark.skipif(os.name == "nt", reason="Requires Linux")
def test_vcan_local():
    try:
        bus = can.Bus(channel="vcan0", interface="socketcan")
        assert bus is not None
    except Exception:
        pytest.skip("vcan0 not available on this system")
