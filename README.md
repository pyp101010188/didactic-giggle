import smbus
import time
import math

bus = smbus.SMBus(1)
addr = 0x68

# Разбудить MPU6050
bus.write_byte_data(addr, 0x6B, 0)

def read_word(reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)

    value = (high << 8) | low

    if value >= 0x8000:
        value = -((65535 - value) + 1)

    return value

while True:
    ax = read_word(0x3B)
    ay = read_word(0x3D)
    az = read_word(0x3F)

    gx = read_word(0x43)
    gy = read_word(0x45)
    gz = read_word(0x47)

    ax_g = ax / 16384.0
    ay_g = ay / 16384.0
    az_g = az / 16384.0

    roll = math.degrees(math.atan2(ay_g, az_g))
    pitch = math.degrees(math.atan2(-ax_g, math.sqrt(ay_g**2 + az_g**2)))

    print(
        f"ACC: {ax:6d} {ay:6d} {az:6d} | "
        f"GYRO: {gx:6d} {gy:6d} {gz:6d} | "
        f"ROLL: {roll:6.1f} | PITCH: {pitch:6.1f}"
    )

    time.sleep(0.2)
