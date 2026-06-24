import can
import struct
import time

CAN_IFACE = "can1"   # у тебя физический CAN0 виден как can1
GEAR_RATIO = 15.0

NODE_IDS = [1, 2, 3, 4]

IDLE = 1
CLOSED_LOOP = 8

bus = can.interface.Bus(channel=CAN_IFACE, interface="socketcan")

def set_state(node_id, state):
    msg = can.Message(
        arbitration_id=(node_id << 5) | 0x07,
        data=struct.pack("<I", state),
        is_extended_id=False
    )
    bus.send(msg)

def set_pos(node_id, motor_turns):
    msg = can.Message(
        arbitration_id=(node_id << 5) | 0x0C,
        data=struct.pack("<fhh", motor_turns, 0, 0),
        is_extended_id=False
    )
    bus.send(msg)

def deg_to_motor_turns(deg):
    return deg / 360.0 * GEAR_RATIO

# Включить closed loop
for node in NODE_IDS:
    set_state(node, CLOSED_LOOP)
    print("CLOSED_LOOP:", node)

time.sleep(1)

# Повернуть все моторы на 25 градусов выхода редуктора
angle_deg = 25
turns = deg_to_motor_turns(angle_deg)

for node in NODE_IDS:
    set_pos(node, turns)
    print("MOVE:", node, angle_deg, "deg =", turns, "motor turns")

print("Готово")
