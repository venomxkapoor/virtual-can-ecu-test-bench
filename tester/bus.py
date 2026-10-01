import can

def get_virtual_bus():
    return can.Bus(channel="test_bus", interface="virtual")

def get_socketcan_bus(channel="vcan0"):
    return can.Bus(channel=channel, interface="socketcan")
