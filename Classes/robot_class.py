import numpy as np

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
        robot_vector = np.array([np.sin(orientation_rad),np.cos(orientation_rad)])
        robot_block_vector = self.position - self.target.position

        self.distance = np.linalg.norm(robot_block_vector)
        print("Distance is:", self.distance)

        sin_angle = np.cross(robot_block_vector, robot_vector) / (np.linalg.norm(robot_vector) * np.linalg.norm(robot_block_vector))
        cos_angle = np.dot(robot_block_vector, robot_vector) / (np.linalg.norm(robot_vector) * np.linalg.norm(robot_block_vector))
        angle_sin = np.arcsin(sin_angle)
        angle_cos = np.arccos(cos_angle)

        if angle_cos > 90:
            self.angle = np.degrees(np.sign(angle_sin)*(-1)*angle_cos)
        else:
            self.angle = np.degrees(-1*angle_sin)
        print("Angle is:", self.angle)

        return self.distance, self.angle  #use self.target

    def move_forward(self):
        """Moves the robot forward"""
        pass

    def move_backward(self):
        """Moves the robot backward"""
        pass

    def turn(self):
        margin = 20
        while np.abs(self.angle) > margin:
            self.coms.turn(15*np.sign(self.angle))  #later the percentage can be decided by a controller
            self.update_position()
            self.distance, self.angle = self.get_distance_angle_target()
        self.coms.turn(0)

    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position) #, self.target, self.orientation, self.distance, self.num_tested, self.num_picked_up)
        #\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}"