"""General Idea:
Function           |Num     Parameter    e.g. forward 50%: b(1) b(0.5) so one byte for num then 1 for parameter
-----------------------------------------
forward            | 0      %power
backward           | 1      %power
turn_clockwise     | 2      %power
turn_anticlockwise | 3      %power
hall_effect request| 4      None
infra_red request  | 5      None




"""
class Coms():
    def __init__(self, position, id):
        """Sets up a communication object"""
        self.open = False

    def send(self, message):
        #serial something

    #Below are the translation functions using scheme above
    def translate_turn(self, power):
        """Sends signal to arduino to set the motor to the specified power"""
        #translate into, pin number

    def translate_forward(self, power):
        """Updates the position of the block"""
        position = new_position
