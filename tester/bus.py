import can

def get_virtual_bus():
    return can.interface.Bus("test_bus", bustype="virtual")

def get_socketcan_bus(channel="vcan0"):
    return can.interface.Bus(channel, bustype="socketcan")
