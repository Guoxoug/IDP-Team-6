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

final_centre = np.array([551, 362])

name = initialise_connection.locate_port().device  # finds port connected to board (Arduino resets on connection)
arduino_port = serial.Serial(name, 9600, timeout=5)  # 5 second timout for read method
initialise_connection.handshake(arduino_port)

arduino_coms = coms_class.Coms(arduino_port)

arduino_coms.stop()
arduino_coms.servo_state("centre")


camera = Camera()
blocks = camera.init_blocks()
robot = Robot(camera, arduino_coms)

conflict, conflict_blocks = camera.check_initial_clear()
if conflict:
    print("Conflicts:", len(conflict_blocks))
    while len(conflict) != 0:
        robot.target = robot.find_next_target(conflict_blocks)

        conflict_blocks.pop(robot.target.id)

        robot.go_towards_target()
        robot.sort_procedure()

        camera.blocks[robot.target.id] = robot.target
    print("Conflicts resolved")
    print("Going towards corner to rotate for line up")
    fake_target = Block(np.array([60,390]), 100)
    robot.target = fake_target
    robot.go_towards_target()
    #####Have to add a bit forward

else:
    robot.simple_forward(1800)
    robot.simple_turn(600, 1)

#Pick up the line of 5 blocks
for i in range(0, 5):
    robot.target = camera.blocks[i]

    robot.go_towards_target()

    robot.sort_procedure()

    #Update main camera.blocks with their object values
    camera.blocks[robot.target.id] = robot.target

#Implement a anticlockwise turn and backward thing?

#Now spread out blocks (remaining):
remaining_blocks = list(filter(lambda x: not x.tested, camera.blocks.values()))

while len(remaining_blocks) != 0:
    robot.target = robot.find_next_target(remaining_blocks)

    remaining_blocks.pop(robot.target.id)

    robot.go_towards_target()

    robot.sort_procedure()

    #Update main camera.blocks with their object values
    camera.blocks[robot.target.id] = robot.target

final_target = Block(final_centre, 101)
print("Going towards final rotating place")
robot.target = final_target
robot.go_towards_target()

#Set sequence
time.sleep(2)
robot.simple_forward(200)
time.sleep(2)
robot.simple_turn(1000, 1)
time.sleep(1)
robot.simple_forward(500)
time.sleep(1)
robot.simple_backward(1000)
time.sleep(1)
robot.simple_forward(150)
robot.drop_off()

print("Mission accomplished (hopefully) returning home")

robot.simple_forward()

arduino_coms.stop()
arduino_port.close()
print("Port closed")

time.sleep(5)

if camera.open:
    camera.close()
    print("Camera closed")



