import os
import cantools
from tester.decoder import DBCDecoder
import can

def test_dbc_decode():
    dbc_path = os.path.join(os.path.dirname(__file__), "..", "..", "dbc", "demo_ecu.dbc")
    db = cantools.database.load_file(dbc_path)
    
    data = db.encode_message("ECU_STATUS", {"state": "RUN", "alive_counter": 5})
    msg = can.Message(arbitration_id=0x100, data=data)
    
    decoder = DBCDecoder(dbc_path)
    decoded = decoder.decode(msg)
    
    assert decoded["state"] == "RUN"
    assert decoded["alive_counter"] == 5
