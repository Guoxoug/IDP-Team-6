import serial
from serial.tools import list_ports
import time

"""connection initialisation module
finds port that board is connected to 
handshake"""


def locate_port():
    """locates usb port that the Arduino is connected to"""
    print("finding port...")
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # iterate through ports and find Arduino connection (ONLY CONNECT 1 ARDUINO AT A TIME)
        if "Arduino" in port.description:
            print("port description: ", port.description)
            return port
    else:
        raise ConnectionError("no Arduino connected")


def handshake(port):
    """handshake with Arduino, port is left open if successful
    Takes Serial object as argument"""

    counter = 0
    while True:
        counter += 1
        if port.read(5).decode("utf-8") == "hello":
            print("hello received")
            port.write(b"H")
            reply = port.read().decode("utf-8")  # don't need sleep as timeout is inside read method
            #  receives reply from Arduino acknowledging PC
            if reply == "H":
                print("handshake complete, port now open")
                break
            else:
                port.close()
                raise Exception("Arduino failed to send acknowledgement")
        elif counter >= 50:  # timeout if no hello from board
            port.close()
            raise TimeoutError("failed to communicate with Arduino")


if __name__ == "__main__":
    # cannot have two programs connected to the same port (i.e. exit Arduino IDE serial monitor)
    # Handshake to check initial connection
    name = locate_port().device  # finds port connected to board (Arduino resets on connection)
    arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
    handshake(arduino_port)

    arduino_port.write(b"J")
    print("received: ", arduino_port.read().decode("utf-8"))
    arduino_port.close()
