import numpy as np
from simple_pid import PID

class Robot():
    def __init__(self, camera, coms):
        """Sets up a Robot object"""
        self.camera = camera
        self.coms = coms
        self.position = False
        self.orientation = False
        self.target = False  #Can assign block object
        self.front = False
        self.back = False
        self.distance = 0
        self.angle = 0
        self.num_tested = 0
        self.num_picked_up = 0
        self.pos_array = []
        self.ori_array = []

        for i in range(0,3):
            next_position, next_orientation = self.camera.get_position_orientation_robot()
            self.pos_array.append(next_position)
            self.ori_array.append(next_orientation)
        print("Length pos_array:", len(self.pos_array))
        print("Length ori_array:", len(self.ori_array))
        self.update_position()

    def update_position(self):
        """Updates the position of the robot using the self.front and self.back circles"""
        #some function camera.update_robot()
        self.pos_array.pop(0)
        self.ori_array.pop(0)
        next_position, next_orientation = self.camera.get_position_orientation_robot()
        self.pos_array.append(next_position)
        self.ori_array.append(next_orientation)
        self.orientation = np.median(self.ori_array)
        self.position = np.median(self.pos_array, axis = 0)
        #print("Updated position:", self.position)
        #print("Updated orientation:", self.orientation)

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
        self.update_position()

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

    def move_forward(self, p=0.5, i=0.1, d=0.1, num=1000):
        """Moves the robot forward"""
        margin_ori = 20
        set_point = 50
        pid = PID(p, i, d, setpoint = set_point)
        self.distance, self.angle = self.get_distance_angle_target()
        pid.output_limits = (-50, 50)
        control = pid(self.distance)
        i = 0

        while(control != 0 and i < num and abs(self.distance-set_point) > 10):
            if np.abs(self.angle) >= margin_ori:
                print("Stopping")
                self.coms.stop()
                self.turn()
            print("Control dist output:", control*-1)
            print("Components dist", pid.components)  # the separate terms are now in p, i, d)
            self.coms.forward(int(control*-1))

            self.distance, self.angle = self.get_distance_angle_target()

            control = pid(self.distance)
            i += 1


        print("Arrived at destination")

        self.coms.stop()
        """
        for i in range(num):
            self.coms.forward(50)
        self.coms.stop()

        self.distance, self.angle = self.get_distance_angle_target()
        while np.abs(self.distance) > margin:
            if np.abs(self.orientation) >= margin_ori:
                self.coms.stop()
                self.turn()
            self.coms.forward(int(30*np.sign(self.distance))) #later the percentage can be decided by a controller
            self.distance, self.angle = self.get_distance_angle_target()  #Has to update the robot pos_ori inside anyway
        self.coms.stop()
        """

    def move_backward(self):
        """Moves the robot backward"""
        pass

    def turn(self, p = 0.5, i = 0.1, d = 0.1, num = 40):
        margin = 10
        pid = PID(p, i, d, setpoint = 0)
        self.distance, self.angle = self.get_distance_angle_target()
        pid.output_limits = (-50, 50)
        control = pid(self.angle)
        i = 0

        while(control != 0 and i < num and abs(self.angle) > 10):
            print("Control output:", control*-1)
            print("Components", pid.components)  # the separate terms are now in p, i, d)
            self.coms.turn(int(control*-1))

            self.distance, self.angle = self.get_distance_angle_target()

            control = pid(self.angle)
            i += 1

        self.coms.stop()
        """
        for i in range(0,num):
            #print(i)
            self.coms.turn(-20)
        self.coms.stop()
        
        
        self.distance, self.angle = self.get_distance_angle_target()
        while np.abs(self.angle) > margin:
            self.coms.turn(int(30*np.sign(self.angle)))  #later the percentage can be decided by a controller
            self.distance, self.angle = self.get_distance_angle_target()  #Has to update the robot pos_ori inside anyway
        self.coms.stop()
        """

    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position) #, self.target, self.orientation, self.distance, self.num_tested, self.num_picked_up)
        #\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}"