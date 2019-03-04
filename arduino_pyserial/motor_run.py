from init_connection import initialise_connection
from Classes import coms_class
import serial
import time
"""1st four lines and last 2 are basic connection requirements
IMPORTS MAY BREAK depending on whether the code is run in an IDE or from the console
"""
name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=1)  # 1 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.forward(100)
time.sleep(2)
arduino_coms.backward(100)
time.sleep(2)
for i in range(6):
    arduino_coms.turn(100, "clockwise")
    time.sleep(0.3)
    arduino_coms.turn(100, "anticlockwise")
    time.sleep(0.3)
arduino_coms.stop()


arduino_port.close()
print("port closed")