import can
import struct

bus = can.interface.Bus(channel="can0", interface="socketcan")

NODE_IDS = [1, 2, 3, 4]

IDLE = 1
ENCODER_OFFSET = 7
CLOSED_LOOP = 8

def set_state(node_id, state):
    msg = can.Message(
        arbitration_id=(node_id << 5) | 0x07,
        data=struct.pack("<I", state),
        is_extended_id=False
    )
    bus.send(msg)
    print("sent node:", node_id, "state:", state)

# стоп всех
for node in NODE_IDS:
    set_state(node, IDLE)

# калибровка энкодеров по очереди
for node in NODE_IDS:
    print("Калибрую encoder offset node", node)
    set_state(node, ENCODER_OFFSET)
    input("Когда мотор остановится, нажми Enter...")

# включить closed loop
for node in NODE_IDS:
    set_state(node, CLOSED_LOOP)

print("Готово")
