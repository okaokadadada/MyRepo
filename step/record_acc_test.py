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
    xh = i2c.read_byte_data(address, 0x32)
    print(f"xh = {xh}")
