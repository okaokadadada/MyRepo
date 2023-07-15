import smbus
import time

#I2C設定
i2c = smbus.SMBus(1)
address = 0x53

#センサーの設定
ret = i2c.write_byte_data(address, 0x2C, 0x0B)
ret = i2c.write_byte_data(address, 0x31, 0x09)
ret = i2c.write_byte_data(address, 0x2D, 0x08)

while True:
    
    #データ読み込み
    xl = i2c.read_byte_data(address, 0x32)
    xh = i2c.read_byte_data(address, 0x33)
    yl = i2c.read_byte_data(address, 0x34)
    yh = i2c.read_byte_data(address, 0x35)
    zl = i2c.read_byte_data(address, 0x36)
    zh = i2c.read_byte_data(address, 0x37)
    
    #データ変換
    out_x = xh << 8 | xl
    out_y = yh << 8 | yl
    out_z = zh << 8 | zl
    
    #極性判断
    if out_x >= 32768:
        out_x = out_x - 65536
    
    if out_y >= 32768:
        out_y = out_y - 65536
    
    if out_z >= 32768:
        out_z = out_z - 65536
    
    #物理量（加速度）に変換
    out_x = out_x * 0.004
    out_y = out_y * 0.004
    out_z = out_z * 0.004
    
    #表示
    print('X: ' + str(out_x))
    print('Y: ' + str(out_y))
    print('Z: ' + str(out_z))
    
    #一時停止
    time.sleep(0.5)
