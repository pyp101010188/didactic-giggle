import smbus
import time
import math

bus = smbus.SMBus(1)
addr = 0x68

bus.write_byte_data(addr, 0x6B, 0)  # wake up

def read_word(reg):
    high = bus.read_byte_data(addr, reg)
    low = bus.read_byte_data(addr, reg + 1)
    value = (high << 8) | low
    if value >= 0x8000:
        value -= 65536
    return value

print("Положи датчик ровно и не трогай...")
time.sleep(2)

N = 500

ax_off = ay_off = az_off = 0
gx_off = gy_off = gz_off = 0

for i in range(N):
    ax_off += read_word(0x3B)
    ay_off += read_word(0x3D)
    az_off += read_word(0x3F)

    gx_off += read_word(0x43)
    gy_off += read_word(0x45)
    gz_off += read_word(0x47)

    time.sleep(0.005)

ax_off /= N
ay_off /= N
az_off = az_off / N - 16384  # Z должен видеть 1g

gx_off /= N
gy_off /= N
gz_off /= N

print("Калибровка готова")
print("Offsets:", ax_off, ay_off, az_off, gx_off, gy_off, gz_off)

while True:
    ax = read_word(0x3B) - ax_off
    ay = read_word(0x3D) - ay_off
    az = read_word(0x3F) - az_off

    gx = read_word(0x43) - gx_off
    gy = read_word(0x45) - gy_off
    gz = read_word(0x47) - gz_off

    ax_g = ax / 16384.0
    ay_g = ay / 16384.0
    az_g = az / 16384.0

    roll = math.degrees(math.atan2(ay_g, az_g))
    pitch = math.degrees(math.atan2(-ax_g, math.sqrt(ay_g**2 + az_g**2)))

    print(
        f"ROLL: {roll:6.2f} | PITCH: {pitch:6.2f} | "
        f"ACC: {ax:7.0f} {ay:7.0f} {az:7.0f} | "
        f"GYRO: {gx:7.0f} {gy:7.0f} {gz:7.0f}"
    )

    time.sleep(0.1)
