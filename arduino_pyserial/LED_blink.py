from arduino_pyserial import initialise_connection
import serial
"""python script that makes the Arduino blink"""

name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)
while True:
    keyboard_input = input("space for on, just enter for off, two spaces for exit")
    if keyboard_input == " ":
        arduino_port.write(0)
    elif keyboard_input == " ":
        arduino_port.write(1)
    elif keyboard_input == " ":
        arduino_port.write(2)
        break

arduino_port.close()
print("port closed")