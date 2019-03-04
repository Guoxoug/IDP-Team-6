import numpy as np
from simple_pid import PID

class Robot():
    def __init__(self, camera):
        """Sets up a Robot object"""
        self.camera = camera
        #self.coms = coms
        self.position = False
        self.orientation = False
        self.target = False  #Can assign block object
        self.front = False
        self.back = False
        self.distance = 0
        self.angle = 0
        self.num_tested = 0
        self.num_picked_up = 0

    def update_position(self):
        """Updates the position of the robot using the self.front and self.back circles"""
        #some function camera.update_robot()
        self.position, self.orientation = self.camera.get_position_orientation_robot()

    def find_next_target(self):
        """Use the camera to find the next destination as position coordinates"""
        pass

    def get_distance(self):
        """Gets the distance of itself (midpoint of circles) relative to Block"""
        #always call update_position before this
        #should be linked with get_orientation
        pass  #use self.target

    def get_distance_angle_target(self):
        """Gets the orientation of itself relative to Block using angle between line of circle-circle and centre-circle
        clockwise is positive rotation
        """
        #always call update_position before this
        self.position, self.orientation = self.camera.get_position_orientation_robot()
        print("Position updated")

        orientation_rad = np.deg2rad(self.orientation)
        vertical_vector = np.array([0,-1])
        robot_block_vector = self.target.position - self.position  #vector from robot to block

        self.distance = np.linalg.norm(robot_block_vector)
        print("Distance is:", self.distance)

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

        print("Angle is:", self.angle)

        return self.distance, self.angle  #use self.target

    def move_forward(self):
        """Moves the robot forward"""
        pass

    def move_backward(self):
        """Moves the robot backward"""
        pass

    def turn(self):
        margin = 10
        pid = PID(1, 0.01, 0.05, setpoint = 0)
        u, v = self.get_distance_angle_target()
        pid.output_limits = (-5, 5)
        control = pid(v)

        while(control != 0):
            print("Control output:", control)
            print("Components", pid.components)  # the separate terms are now in p, i, d)
            self.coms.turn(control)

            u, v = self.get_distance_angle_target()

            control = pid(v)
        """

        while np.abs(self.angle) > margin:
            self.coms.turn(10*np.sign(self.angle))  #later the percentage can be decided by a controller
            self.distance, self.angle = self.get_distance_angle_target()  #Has to update the robot pos_ori inside anyway
        self.coms.turn(0)
        """
    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position) #, self.target, self.orientation, self.distance, self.num_tested, self.num_picked_up)
        #\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}"