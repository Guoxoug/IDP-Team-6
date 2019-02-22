class Robot():
    def __init__(self, position):
        """Sets up a Robot object"""
        self.position = position
        self.target = None  #Can assign block object
        self.front = None
        self.back = None
        self.orientation = 0
        self.distance = 0
        self.num_tested = 0
        self.num_picked_up = 0

    def update_position(self):
        """Updates the position of the robot using the self.front and self.back circles"""
        pass

    def find_next_target(self):
        """Use the camera to find the next destination as position coordinates"""
        pass

    def get_distance(self):
        """Gets the distance of itself (midpoint of circles) relative to Block"""
        #always call update_position before this
        #should be linked with get_orientation
        pass  #use self.target

    def get_orientation(self, Block):
        """Gets the orientation of itself relative to Block using angle between line of circle-circle and centre-circle"""
        #always call update_position before this
        pass  #use self.target

    def move_forward(self):
        """Moves the robot forward"""
        pass

    def move_backward(self):
        """Moves the robot backward"""
        pass

    def turn(self):
        angle = get_orientation()
        while angle > margin:
            robocoms(turn, 50%)  #later the percentage can be decided by a controller
            update_position()
            angle = get_orientation()
        robocoms(turn, False)

    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position, self.target.position, self.orientation, self.distance, self.num_tested, self.num_picked_up)