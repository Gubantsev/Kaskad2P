import serial.tools.list_ports

list = serial.tools.list_ports.comports()
print(list)

