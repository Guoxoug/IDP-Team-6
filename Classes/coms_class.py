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



    def motor(self, power: int, motor_name: str):
        #  takes power and motor name (right, left)  as parameters
        #  power is between -100 and 100
        #  power to arduino func takes 0 - 255
        command = bytearray([])
        if motor_name == "right":
            if power >= 0:
                input_power = round(power / 100 * 255)
                command += b"a"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                print("command: ", command)
                self.serial.write(command)


            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"b"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.serial.write(command)
                print("command: ", command)
        if motor_name == "left":
            if power >= 0:
                input_power = round(power / 100 * 255)
                command += b"c"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.serial.write(command)
                print("command: ", command)
            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"d"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.serial.write(command)
                print("command: ", command)
    # Movement methods
    # Self explanatory ^^
    # power always int 0-100
    def forward(self, power):
        self.motor(power, "right")
        self.motor(power, "left")

    def backward(self, power):
        self.motor(-power, "right")
        self.motor(-power, "left")

    def turn(self, power, direction: str):
        if direction == "clockwise":
            self.motor(-power, "right")
            self.motor(power, "left")
        if direction == "anticlockwise":
            self.motor(power, "right")
            self.motor(-power, "left")

    def stop(self):
        self.motor(0, "right")
        self.motor(0, "left")

    def servo(self, position: int):
        """sets position of servo in degrees 0- 180"""
        position = int(position) # bytes only takes ints
        command = bytearray([])
        command += b"e"
        command += bytes([position])
        command += b"\n"
        print("command: ", command)
        # newline indicates end of command to arduino
        self.serial.write(command)
