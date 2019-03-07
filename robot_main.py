from init_connection import initialise_connection
from Classes import coms_class
import serial
import time
from Classes.block_class import Block
from Classes.robot_class import Robot
import cv2
import numpy as np
from Classes.coms_class import Coms
from Classes.camera_class import Camera
"""1st four lines and last 2 are basic connection requirements
IMPORTS MAY BREAK depending on whether the code is run in an IDE or from the console
"""


name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.stop()

camera = Camera()
blocks = camera.init_blocks()
robot = Robot(camera, arduino_coms)

robot.target = find_next_target(blocks)
robot.go_towards_target()

#check IR
#if yes, check hall effect update block.tested and block.nuclear
#if safe:
arduino_coms.servo_state("left")
#         drop down and slide across arduino_coms something

#Loop again until no more block.tested = False


arduino_coms.stop()
arduino_port.close()
print("Port closed")

time.sleep(10)

if camera.open:
    camera.close()
    print("Camera closed")



