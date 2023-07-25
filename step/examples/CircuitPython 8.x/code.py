# SPDX-FileCopyrightText: Copyright (c) 2022 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_adxl37x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
accelerometer = adafruit_adxl37x.ADXL375(i2c)

while True:
    # print(accelerometer.acceleration)
    x, y, z = accelerometer.acceleration
    x = x-3
    y = y+5 
    z = z-4
    print("x={：．4f},y={:.4f},z={:.4f}".format(x, y, z))
    # print("x=%f, y=%f,z=%f m/s^2" % accelerometer.acceleration)
    time.sleep(0.2)
