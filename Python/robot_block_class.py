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


    def __repr__(self):
        return "Robot\n position: {}\n target position: {}\n orientation: {}\n distance: {}\n number tested: {}\n number picked up: {}".format(self.position, self.target.position, self.orientation, self.distance, self.num_tested, self.num_picked_up)



class Block():
    def __init__(self, position, id):
        """Sets up a Block object"""
        self.position = position
        self.tested = False
        self.nuclear = None
        self.picked_up = False
        self.assigned = False
        self.id = id

    def update_position(self, new_position):
        """Updates the position of the block"""
        position = new_position

    def __repr__(self):
        return "Block {}:\n position: {}\n tested: {}\n nuclear: {}\n picked_up: {}\n assigned: {}".format(self.id, self.position, self.tested, self.nuclear, self.picked_up, self.assigned)
