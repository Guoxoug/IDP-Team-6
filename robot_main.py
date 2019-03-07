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
"""
name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.stop()
"""


camera = Camera()

blocks = camera.init_blocks()

#robot = Robot(camera, arduino_coms)
robot.target = find_next_target(blocks)

robot.go_towards_target()
#check IR
#if yes, check hall effect
#

#blocks = camera.init_blocks()
#block_target = Block(np.array([314, 32]),0)
#robot.target = block_target
i = 0

#robot.turn(0.5, 0.1, 0.1, 40)
#robot.move_forward(0.5, 0.1, 0.1, 1000)


#turn speed 20, 90° for 875
#robot.move_forward(1000) 1200 halfway across red to white line

"""
blocks = camera.init_blocks()

block_target = blocks[0]
print("Set target")
print(block_target)
robot.target = block_target

distance, angle = robot.get_distance_angle_target()

print("Starting to turn", angle)

time.sleep(10)

robot.turn()

arduino_coms.stop()


arduino_port.close()
print("port closed")


"""

time.sleep(10)

if camera.open:
    print("Closing")
    camera.close()




