import numpy as np
from simple_pid import PID
from scipy.optimize import minimize_scalar
from statistics import mode
import cv2
import time


class Robot:
    def __init__(self, camera, coms):
        """Sets up a Robot object"""
        self.camera = camera
        self.coms = coms  #communications module for the arduino
        self.position = False
        self.orientation = False
        self.target = False  # Can assign block object
        self.distance = 0 #Distance from target
        self.angle = 0  #Angle from target
        self.pos_array = []
        self.ori_array = []

        #Initialise the array where the last three positions and orientations are stored in
        for i in range(0, 3):
            frame, next_position, next_orientation = self.camera.get_position_orientation_robot()
            self.pos_array.append(next_position)
            self.ori_array.append(next_orientation)
        print("Length pos_array:", len(self.pos_array))
        print("Length ori_array:", len(self.ori_array))
        self.update_position()


    def update_position(self):
        """Updates the position of the robot by analysing another image and taking the median of the last three"""
        self.pos_array.pop(0)
        self.ori_array.pop(0)

        #Get the newest position and orientation from the camera class
        frame, next_position, next_orientation = self.camera.get_position_orientation_robot()

        self.pos_array.append(next_position)
        self.ori_array.append(next_orientation)

        #Take the median of the last three as the new position and orientation
        self.orientation = np.median(self.ori_array)
        self.position = np.median(self.pos_array, axis=0)

        #Draw on the current frame with an arrow starting at the position
        # in the direciton of the orientation
        position_arrow = self.position + 45 * np.array([np.sin(np.deg2rad(self.orientation)),
                                                        -np.cos(np.deg2rad(self.orientation))])
        cv2.arrowedLine(frame, tuple(self.position), tuple(position_arrow.astype(int)), (0, 255, 0), 2)
        cv2.imshow("Centroid", frame)
        cv2.waitKey(5)

    def find_next_target(self, blocks):
        """Given a dictionary of blocks it will return the closest one to be used as its next target"""
        blocks_sorted = sorted(blocks.values(), key=lambda x: self.get_distance_angle_target(x))

        print("Assigning...")
        blocks_sorted[0].assigned = True

        return blocks_sorted[0]

    def go_towards_target(self):
        """Turns and moves towards the target, returns True if there"""

        self.turn()
        self.move_forward()
        print("Arrived at destination")
        return True

    def specified_turn(self):
        """Determines the last turn when robot is against wall next to platform such that after the turn the
            platform is aligned with our lift"""
        power_left = -2
        power_right = -100
        self.coms.LED_flash("on")
        num = 367
        for i in range(0, num):
            self.coms.motor(power_right, "right")
            self.coms.motor(1.05 * power_left, "left")
        self.coms.stop()

        #Go further backwards and then slightly forward so blocks are against the back of the robot for sweeper
        self.simple_backward(275)
        self.simple_forward(125)
        return True

    def nuclear_check(self):
        """Uses the hall effect sensor to check for a magnetic field, takes the mode of 10 readings"""
        nuclear_output = 2
        outputs = []

        print("Checking hall effect sensor")
        while len(outputs) <= 10:
            nuclear_output = self.coms.hall_effect()

            if nuclear_output != 2:
                outputs.append(nuclear_output)

        nuclear_output = mode(outputs)
        print("Output HE received:", nuclear_output, type(nuclear_output))

        #Update the block variables
        if nuclear_output == 1:
            print("Nuclear")
            self.target.tested = True
            self.target.nuclear = True
            return True
        elif nuclear_output == 0:
            print("Safe")
            self.target.tested = True
            self.target.nuclear = False
            return False

    def IR_check(self):
        """Similar to nuclear_check but now checking the IR sensor for a positive reading indicating
            a block is present"""
        IR_output = 2

        while IR_output == 2:
            print("Checking IR sensor")
            IR_output = self.coms.IR_sensor()

        print("Output IR received:", IR_output, type(IR_output))

        if IR_output == 1:
            self.target.present = True
            return True
        elif IR_output == 0:
            self.target.present = False
            return False
        else:
            raise ValueError("IR_output is not 1 or 0, see above")

    def sort(self):
        """Using the target block variables it will sort them into the correct side"""
        if self.target.tested == True:
            if self.target.nuclear == True:
                print("Flushing")
                self.coms.servo_state("right")
                time.sleep(0.5)
                self.simple_forward(180)
                time.sleep(0.5)
                self.coms.servo_state("left")
                time.sleep(0.5)
                self.coms.servo_state("centre")
                time.sleep(0.5)
                self.simple_backward(300)     #simple backward 300
                return True

            else:
                print("Placing in holding area")
                self.coms.servo_state("left")
                time.sleep(0.5)
                self.simple_forward(180)
                time.sleep(0.5)
                self.coms.servo_state("centre")
                self.simple_backward(300)
                return True

        else:
            print("Attempting to sweep but not yet tested")
            return False

    def sort_procedure(self):
        """Combines all the functions required to sort a block"""
        self.IR_check()
        self.coms.forward(30)
        i = 0

        #Whilst robot is moving at speed of 30 check IR sensor and stop when a positive reading is given
        while self.target.present == False and i < 1000:
            self.IR_check()

            # i iterations is in case it accidentally missed the block so that it won't go forward forever
            i += 1

        if i < 1000:
            #When a block is found do the folllowing
            self.coms.stop()

            self.simple_forward(75)
            self.nuclear_check()
            self.sort()

            print("Sort procedure finished")
            return True
        else:
            #Missed the block somehow, simply back up
            print("Didn't come up on IR")
            self.simple_backward(300)
            return True

    def drop_off(self):
        "Starts the sweep and lift procedure"
        self.coms.offload()
        return True

    def get_distance_angle_target(self, target):
        """Gets the orientation of itself relative to Block clockwise is positive rotation"""
        self.update_position()

        orientation_rad = np.deg2rad(self.orientation)  #orientation is relative to a vertical upwards vector
        vertical_vector = np.array([0,-1])
        robot_block_vector = target.position - self.position  #vector from robot to block

        self.distance = np.linalg.norm(robot_block_vector)

        sin_angle = np.cross(vertical_vector, robot_block_vector) / (1 * self.distance)
        cos_angle = np.dot(robot_block_vector, vertical_vector) / (1 * self.distance)
        angle_sin = np.arcsin(sin_angle)
        angle_cos = np.arccos(cos_angle)

        if np.sign(angle_sin) == 1:
            block_angle = angle_cos
        else:
            block_angle = -1*angle_cos

        self.angle = np.degrees(block_angle - orientation_rad)
        if self.angle > 180:
            self.angle = -1*(self.angle-180)
        elif self.angle < -180:
            self.angle = -1*(self.angle+180)

        #In case a block approaches it even though it is not expecting it still sort it accordingly
        if self.coms.IR_sensor() == 1:
            self.simple_forward(75)
            nuclear_test = self.nuclear_check()
            if nuclear_test:
                self.coms.servo_state("right")
            elif nuclear_test == False:
                self.coms.servo_state("left")
            time.sleep(0.5)
            self.simple_forward(180)
            time.sleep(0.5)
            self.coms.servo_state("centre")
            self.simple_backward(300)


        return self.distance, self.angle

    def move_forward(self, p=0.5, i=0.1, d=0.1, s_p = 40):
        """Moves the robot forward using a PID controller"""
        margin_ori = 20
        pid = PID(p, i, d, setpoint = s_p)
        #pid.proportional_on_measurement = True
        pid.output_limits = (-50, 50)

        self.distance, self.angle = self.get_distance_angle_target(self.target)
        control = pid(self.distance)
        i = 0

        while(control != 0 and abs(self.distance-s_p) > 10):
            control = pid(self.distance)

            #If the angle between the block and robot exceeds margin_ori, stop and align again
            if np.abs(self.angle) >= margin_ori:
                print("Stopping")
                self.coms.stop()
                self.turn()

            if np.abs(control) > 10:
                self.coms.forward(int(control*-1))
            else:
                #forward less than 10 doesn't actually move so take a lower bound of 10
                self.coms.forward(int(10*-1))

            self.distance, self.angle = self.get_distance_angle_target(self.target)
            print("Distance away:", self.distance)

        print("Stopped moving forward")

        self.coms.stop()

    def simple_backward(self, num):
        """Simple function that goes backward for num iterations"""
        for i in range(0, num):
            self.coms.backward(50)
        self.coms.stop()

    def simple_forward(self, num, speed = 50):
        """Simple function that goes backward for num iterations"""
        for i in range(0, num):
            self.coms.forward(speed)  #
        self.coms.stop()

    def simple_turn(self, num, sign):
        """Simple function that turns for num iterations"""
        for i in range(0, num):
            self.coms.turn(int(np.sign(sign)*20))
        self.coms.stop()

    def turn(self, p = 0.5, i = 0.1, d = 0.1, margin = 10, on_measure = False):
        """Aligns itself with target using a PID controller"""
        pid = PID(p, i, d, setpoint = 0)
        self.distance, self.angle = self.get_distance_angle_target(self.target)

        pid.output_limits = (-50, 50)
        control = pid(self.angle)

        pid.proportional_on_measurement = on_measure

        while(control != 0 and abs(self.angle) > margin):
            self.coms.turn(int(control*-1))

            self.distance, self.angle = self.get_distance_angle_target(self.target)
            print("Angle is:", self.angle)

            control = pid(self.angle)

        print("Stopped turning")

        self.coms.stop()

    def __repr__(self):
        """Print function with useful information about the robot"""
        return "Robot\n position: {}\n orientation: {}\n target: {}\n distance: {}\n angle: {}".format(self.position, self.orientation, self.target, self.distance, self.angle)
