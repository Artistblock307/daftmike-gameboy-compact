import os
import serial
import sys
import time

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
time.sleep(.2)

x = ser.readline()
y = str(x)
z = (y[2:-5])

print(z)

if x == 'Hello world':
    ser.write(b'check')