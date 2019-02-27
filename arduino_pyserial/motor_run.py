from init_connection import initialise_connection
from Classes import coms_class
import serial
import time
name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.forward(100)
time.sleep(2)
arduino_coms.backward(100)
time.sleep(2)
arduino_coms.turn(100, "clockwise")
time.sleep(2)
arduino_coms.turn(100, "anticlockwise")
time.sleep(2)
arduino_coms.stop()


arduino_port.close()
print("port closed")