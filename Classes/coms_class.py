from init_connection import initialise_connection

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
    """All messages are """
    def __init__(self, serial):
        """Sets up a communication object"""
        self.serial = serial  # Serial object

    def send(self, message):
        # serial something
        # message in bytes
        self.serial.write(message)

    #Below are the translation functions using scheme above
    def translate_turn(self, power):
        """"""

    def motor(self, power):
        #  power is between -100 and 100
        #  power to arduino func takes 0 - 7
        if power >= 0:
            motor_direction = "f"
            input_power = str(round(power / 100 * 7))
            command = motor_direction + input_power + "\n"  # newline indicates end of command to arduino
            self.serial.write(bytes(command, "utf-8"))  # single character
        if power < 0:
            motor_direction = "b"
            input_power = str(round(-power/100*7))
            command = motor_direction + input_power + "\n"
            self.serial.write(bytes(command, "utf-8"))  # two character string

