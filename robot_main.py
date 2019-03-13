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

final_centre = np.array([531, 362])
middle_stop = np.array([240, 400])
drop_off = np.array([531, 562])
first_location = np.array([70, 390])
rotate = np.array([579, 350])
align_2 = np.array([779, 350])
align = np.array([-50, 50])   #previously 10, 50
home = np.array([540, 440])

name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.stop()
arduino_coms.servo_state("centre")

camera = Camera(arduino_coms)
blocks = camera.init_blocks().copy()
robot = Robot(camera, arduino_coms)

middle_blocks = blocks.copy()
for i in range(0,5):
    middle_blocks.pop(i)
print("Middle blocks", middle_blocks)

for i in range(5, len(blocks)):
    robot.target = robot.find_next_target(middle_blocks)

    middle_blocks.pop(robot.target.id)

    robot.go_towards_target()

    robot.sort_procedure()

    #Update main camera.blocks with their object values
    camera.blocks[robot.target.id] = robot.target

#GOING FOR LINE OF FIVE
middle_stop_block = Block(middle_stop, 105)
first_location_block = Block(first_location,103)
align_block = Block(align, 104)

robot.target = middle_stop_block
robot.go_towards_target()

robot.target = first_location_block
robot.turn()
robot.move_forward(s_p = 30)

time.sleep(3)

robot.target = align_block
robot.turn(margin = 5)

time.sleep(3)

#Pick up the line of 5 blocks
for i in range(0, 5):

    robot.target = camera.blocks[i]

    robot.sort_procedure()

    #Update main camera.blocks with their object values
    camera.blocks[robot.target.id] = robot.target

#########
#DROPPING OFF
rotate_block = Block(rotate,101)
align_2_block = Block(align_2,102)

robot.target = rotate_block
robot.turn(p= 0.2, d = 0.2)
robot.move_forward(p=0.2, d=0.2, s_p = 10)

time.sleep(1)

print("aligning")
robot.target = align_2_block
robot.turn()

time.sleep(1)

robot.simple_forward(500)
time.sleep(1)
robot.specified_turn()

robot.drop_off()

############

print("Mission accomplished (hopefully) returning home")

home_target = Block(home, 102)
print("Going home...")
robot.target = home_target
robot.go_towards_target()
robot.simple_forward(250)
print("Arrived, going to sleep")

arduino_coms.stop()
arduino_port.close()
print("Port closed")

time.sleep(5)

if camera.open:
    camera.close()
    print("Camera closed")



