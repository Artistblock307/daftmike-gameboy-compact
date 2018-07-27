import os
import serial
import sys
import time

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
time.sleep(.5)

x = ser.readline()
y = str(x)
z = (y[2:-5])

print(z)

if z == "Hello world":
    ser.write(b"check")
    x = ser.readline()
