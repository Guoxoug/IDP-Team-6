class Block():
    def __init__(self, position):
        """Sets up a Block object"""
        self.position = position
        self.tested = False
        self.nuclear = None
        self.picked_up = False
        self.assigned = False

    def update_position(self, new_position):
        """Updates the position of the block"""
        position = new_position

    def __repr__(self):
        return "Block {}:\n position: {}\n tested: {}\n nuclear: {}\n picked_up: {}\n assigned: {}".format(self.id, self.position, self.tested, self.nuclear, self.picked_up, self.assigned)
