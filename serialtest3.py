import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

ser.write(b'google')
input = ser.read(6)
print("Read input", input.decode("utf-8") ,"from Arduino")
