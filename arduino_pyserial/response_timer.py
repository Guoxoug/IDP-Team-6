import serial
from timeit import default_timer
from arduino_pyserial import initialise_connection
"""something to time the latency between PC and Arduino"""

name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)
counter = 0
start = default_timer()
while counter < 1000:
    """repeatedly dialogues with arduino"""
    arduino_port.write(b"1")
    arduino_port.read()
    counter +=1
end = default_timer()
time = end - start
time /= 1000
print("single back and forth took: ", time)
arduino_port.close()
print("port closed")
