import pytest
import os
import can

@pytest.mark.skipif(os.name == "nt", reason="Requires Linux")
def test_vcan_local():
    try:
        bus = can.interface.Bus("vcan0", bustype="socketcan")
        assert bus is not None
    except Exception:
        pytest.skip("vcan0 not available on this system")
