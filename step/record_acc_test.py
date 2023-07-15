import smbus
import time

#I2C設定
i2c = smbus.SMBus(1)
address = 0x53

#センサーの設定
# ret = i2c.write_byte_data(address, 0x2C, 0x0B)
# ret = i2c.write_byte_data(address, 0x31, 0x09)
ret = i2c.write_byte_data(address, 0x2D, 0x08)
ret = i2c.write_byte_data(address, 0x31, 0x0b)

while True:
    
    #データ読み込み
    x1 = i2c.read_byte_data(address, 0x32)
    x2 = i2c.read_byte_data(address, 0x33)
    y1 = i2c.read_byte_data(address, 0x34)
    y2 = i2c.read_byte_data(address, 0x35)
    z1 = i2c.read_byte_data(address, 0x36)
    z2 = i2c.read_byte_data(address, 0x37)

    x1_shift = x1 << 8
    x2_shift = x2 << 8
    y1_shift = y1 << 8
    y2_shift = y2 << 8
    z1_shift = z1 << 8
    z2_shift = z2 << 8

    print("------------")
    print(bin(x1_shift))
    print(bin(x2_shift))
    print(bin(y1_shift))
    print(bin(y2_shift))
    print(bin(z1_shift))
    print(bin(z2_shift))
    print("------------")
    print(bin(x1))
    print(bin(x2))
    print(bin(y1))
    print(bin(y2))
    print(bin(z1))
    print(bin(z2))
    print("------------")
    print(x1)
    print(x2)
    print(y1)
    print(y2)
    print(z1)
    print(z2)

    time.sleep(0.5)
