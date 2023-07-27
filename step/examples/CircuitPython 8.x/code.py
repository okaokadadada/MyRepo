# SPDX-FileCopyrightText: Copyright (c) 2022 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_adxl37x
import numpy as np
import datetime
import csv

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
accelerometer = adafruit_adxl37x.ADXL375(i2c)

folder_name = "record"
now = datetime.datetime.now()
file_name = folder_name + '/log_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'


while True:
    # print(accelerometer.acceleration)
    x, y, z = accelerometer.acceleration
    x = x-3
    y = y+5.8 
    z = z+10
    norm = np.sqrt(x*x + y*y + z*z)
    print("norm={:.4f},x={:.4f},y={:.4f},z={:.4f}".format(norm, x, y, z))
    # print("x=%f, y=%f,z=%f m/s^2" % accelerometer.acceleration)
    data_csv = [norm, x, y, z]
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_csv)
    
    time.sleep(0.2)
