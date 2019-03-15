class Block():
    def __init__(self, position, id):
        """Sets up a Block object"""
        self.id = id
        self.position = position
        self.tested = False
        self.present = False
        self.nuclear = None
        self.assigned = False

    def __repr__(self):
        """Print function with relevant information"""
        return "Block {}:\n position: {}\n tested: {}\n nuclear: {}\n presesnt: {}\n assigned: {}".format(self.id, self.position, self.tested, self.nuclear, self.present, self.assigned)
