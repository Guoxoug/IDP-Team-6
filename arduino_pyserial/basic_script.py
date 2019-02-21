import serial
from serial.tools import list_ports
import time

"""Simple script that locates the usb port that the Arduino is connected to and sends a basic instruction"""


def locate_port():
    """locates usb port that the Arduino is connected to"""
    print("finding port...")
    ports = serial.tools.list_ports.comports()
    for port in ports:

        if "Arduino" in port.description:
            print("port description: ", port.description)
            return port
    else:
        raise ConnectionError("no Arduino connected")



    # iterate through ports and find Arduino connection (ONLY CONNECT 1 ARDUINO AT A TIME)


if __name__ == "__main__":
    # cannot have two programs connected to the same port (i.e. exit Arduino IDE serial monitor)
    # Handshake to check initial connection
    name = locate_port().device  # finds port connected to board (Arduino resets on connection)
    arduino_port = serial.Serial(name, 9600)
    counter = 0
    while True:
        counter +=1
        if arduino_port.read(5).decode("utf-8") == "Hello":
            arduino_port.write(b"H")
            print("handshake complete")
            break
        elif counter >= 50:
            arduino_port.close()
            raise TimeoutError("failed to communicate with Arduino")
            break

    arduino_port.write(b"J")
    print("received: ", arduino_port.read().decode("utf-8"))
    print("received: ", arduino_port.read().decode("utf-8"))
    arduino_port.close()
