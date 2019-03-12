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
        self.coms = coms
        self.position = False
        self.orientation = False
        self.target = False  # Can assign block object
        self.front = False
        self.back = False
        self.distance = 0
        self.angle = 0
        self.num_tested = 0
        self.num_picked_up = 0
        self.pos_array = []
        self.ori_array = []

        for i in range(0, 3):
            frame, next_position, next_orientation = self.camera.get_position_orientation_robot()
            self.pos_array.append(next_position)
            self.ori_array.append(next_orientation)
        print("Length pos_array:", len(self.pos_array))
        print("Length ori_array:", len(self.ori_array))
        self.update_position()


    def update_position(self):
        """Updates the position of the robot using the self.front and self.back circles"""
        # some function camera.update_robot()
        self.pos_array.pop(0)
        self.ori_array.pop(0)
        frame, next_position, next_orientation = self.camera.get_position_orientation_robot()
        self.pos_array.append(next_position)
        self.ori_array.append(next_orientation)

        self.orientation = np.median(self.ori_array)
        self.position = np.median(self.pos_array, axis=0)

        position_arrow = self.position + 45 * np.array([np.sin(np.deg2rad(self.orientation)),
                                                        -np.cos(np.deg2rad(self.orientation))])
        cv2.arrowedLine(frame, tuple(self.position), tuple(position_arrow.astype(int)), (0, 255, 0), 2)
        cv2.imshow("Centroid", frame)
        cv2.waitKey(5)

    def find_next_target(self, blocks):
        """Use the camera to find the next destination as position coordinates"""
        blocks_sorted = sorted(blocks.values(), key=lambda x: self.get_distance_angle_target(x))

        print("Assigning...")
        blocks_sorted[0].assigned = True

        return blocks_sorted[0]

    def go_towards_target(self):
        """Turns and moves towards the target, returns True if there"""

        self.turn()
        self.move_forward()
        print("Arrived at destination")

        # print("Final push")
        # for i in range(0, 500):
        #     self.coms.forward(50)

    def nuclear_check(self):
        nuclear_output = 2
        outputs = []

        print("Checking hall effect sensor")
        while len(outputs) <= 10:
            nuclear_output = self.coms.hall_effect()

            if nuclear_output != 2:
                outputs.append(nuclear_output)

        nuclear_output = mode(outputs)
        print("Output HE received:", nuclear_output, type(nuclear_output))

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
        """
        IR_output = 2

        while IR_output == 2:
            print("Checking IR sensor")
            IR_output = self.coms.IR_sensor()

        print("Output IR received:", IR_output, type(IR_output))

        if IR_output == 0:
            self.target.present = True
            return True
        elif IR_output == 1:
            self.target.present = False
            return False
        else:
            raise ValueError("IR_output is not 1 or 0, see above")
        """
        IR_output = 2

        while IR_output == 2:
            print("Checking IR sensor")
            IR_output = self.coms.IR_sensor()

        print("Output IR received:", IR_output, type(IR_output))
        return IR_output

    def sort(self):
        if self.target.tested == True:
            if self.target.nuclear == True:
                print("Flushing")
                self.coms.servo_state("right")
                time.sleep(0.5)
                self.simple_forward(140)
                time.sleep(0.5)
                self.coms.servo_state("centre")
                return True

            elif self.target.nuclear == False:
                print("Placing in holding area")
                self.coms.servo_state("left")
                time.sleep(0.5)
                self.simple_forward(140)
                time.sleep(0.5)
                self.coms.servo_state("centre")
                return True
        else:
            print("Attempting to sweep but not yet tested")
            return False

    def sort_procedure(self):
        self.IR_check()
        self.coms.forward(50)
        while self.target.present == False:
            self.IR_check()
        self.coms.stop()

        self.simple_forward(75)
        self.nuclear_check()
        self.sort()

        print("Sort procedure finished")
        return True

    def drop_off(self):
        self.coms.offload()
        return True

    def get_distance_angle_target(self, target):
        """Gets the orientation of itself relative to Block using angle between line of circle-circle and centre-circle
        clockwise is positive rotation
        """
        #always call update_position before this
        self.update_position()

        orientation_rad = np.deg2rad(self.orientation)
        vertical_vector = np.array([0,-1])
        robot_block_vector = target.position - self.position  #vector from robot to block

        self.distance = np.linalg.norm(robot_block_vector)
        #print("Distance is:", self.distance)

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

        #print("Angle is:", self.angle)

        return self.distance, self.angle  #use self.target

    def move_forward(self, p=0.5, i=0.1, d=0.1, s_p = 40):
        """Moves the robot forward"""
        margin_ori = 20
        pid = PID(p, i, d, setpoint = s_p)
        #pid.proportional_on_measurement = True
        pid.output_limits = (-50, 50)

        self.distance, self.angle = self.get_distance_angle_target(self.target)
        control = pid(self.distance)
        i = 0

        while(control != 0 and abs(self.distance-s_p) > 10):
            control = pid(self.distance)

            if np.abs(self.angle) >= margin_ori:
                print("Stopping")
                self.coms.stop()
                self.turn()

            #print("Control dist output:", control*-1)
            #print("Components dist", pid.components) # the separate terms are now in p, i, d)
            if np.abs(control) > 10:
                self.coms.forward(int(control*-1))
            else:
                self.coms.forward(int(10*-1))

            self.distance, self.angle = self.get_distance_angle_target(self.target)
            print("Distance away:", self.distance)

        print("Stopped moving forward")

        self.coms.stop()

    def simple_backward(self, num):
        for i in range(0, num):
            self.coms.backward(50)
        self.coms.stop()

    def simple_forward(self, num, speed = 50):
        for i in range(0, num):
            self.coms.forward(speed)  #
        self.coms.stop()

    def simple_turn(self, num, sign):
        #Positive, clockwise
        for i in range(0, num):
            self.coms.turn(int(np.sign(sign)*20))
        self.coms.stop()

    def check_validity_turn(self):
        c_o_rotation = self.position + 52*np.array([np.sin(self.orientation), np.cos(self.orientation)])
        print("Self.position:", self.position)
        print("Centre of rotation:", c_o_rotation)

        #Coordinates of corners_robot relative to centre of rotation when self.orientation = 0
        corners_robot = np.array([[50, 18], [-50, 18], [50, -107], [-50, -107]])
        corner_vectors = [corner-c_o_rotation for corner in corners_robot]

        abs_angle_rotation = self.orientation+self.angle

        min_x = 0
        for vector in corner_vectors:
            if np.sign(abs_angle_rotation) == 1:
                min_x_c = minimize_scalar(lambda x: np.cos(x) * vector[0] - np.sin(x) * vector[1], bounds=[0,abs_angle_rotation], method='bounded')
            else:
                min_x_c = minimize_scalar(lambda x: np.cos(x) * vector[0] - np.sin(x) * vector[1], bounds=[abs_angle_rotation, 0], method='bounded')
            print("Min_x_c:", min_x_c)
            min_x = min(min_x, min_x_c)

        print("Min_x", min_x)
        print("Most left point it would hit:", (self.position[0] + min_x))

        if (self.position[0] + min_x) < 23:
            print("It is not safe to turn this way")
            return False
        else:
            return True

    def turn(self, p = 0.5, i = 0.1, d = 0.1, margin = 10, on_measure = False):
        pid = PID(p, i, d, setpoint = 0)
        self.distance, self.angle = self.get_distance_angle_target(self.target)
        #Could implement a check for validity, if not valid, turn the other way

        pid.output_limits = (-50, 50)
        control = pid(self.angle)

        pid.proportional_on_measurement = on_measure

        while(control != 0 and abs(self.angle) > margin):
            #print("Control output:", control*-1)
            #print("Components", pid.components)  # the separate terms are now in p, i, d)
            self.coms.turn(int(control*-1))

            self.distance, self.angle = self.get_distance_angle_target(self.target)
            print("Angle is:", self.angle)

            control = pid(self.angle)

        self.coms.stop()

    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position) #, self.target, self.orientation, self.distance, self.num_tested, self.num_picked_up)
        #\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}"