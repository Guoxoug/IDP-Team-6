from init_connection import initialise_connection
import numpy as np
import time

#servo 2 for sorter
# M1 right
#m2 left
#m3 pulley
#m4 pusher

class Coms():
    """All messages are """
    def __init__(self, serial):
        """Sets up a communication object"""
        self.serial = serial  # Serial object

    def send(self, message: bytearray):
        # serial something
        # message in bytes
        if message[1] == b'\n':  # bytes value of 10 is \n in utf and ascii
            message[1] = bytes([11])
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
                self.send(command)


            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"b"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)
        if motor_name == "left":
            if power >= 0:
                input_power = round(power / 100 * 255)
                command += b"c"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)
            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"d"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)
        if motor_name == "pulley":
            if power >= 0:
                input_power = round(power / 100 * 255)
                command += b"f"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)

            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"g"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)

        if motor_name == "pusher":
            if power >= 0:
                input_power = round(power / 100 * 255)
                command += b"h"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)

            elif power < 0:
                input_power = -round(power / 100 * 255)
                command += b"i"
                command += bytes([input_power])
                command += b"\n"
                # newline indicates end of command to arduino
                self.send(command)

    # power always int 0-100
    def forward(self, power):
        self.motor(power, "right")
        self.motor(1.01*power, "left")

    def backward(self, power):   #red left, white right
        self.motor(-power, "right")
        self.motor(-1.01*power, "left")

    def turn(self, power):
        if np.sign(power) == 1:
            self.motor(-power, "right")
            self.motor(power, "left")
        else:
            self.motor(power, "right")
            self.motor(-power, "left")

    def stop(self):
        self.motor(0, "right")
        self.motor(0, "left")

    def servo(self, position: int):
        """sets position of servo in degrees 0- 180
        NB 78 is centre, angles are measured anticlockwise
        testing shows it can swing +-30 degrees without getting stuck"""

        position = int(position) # bytes only takes ints
        command = bytearray([])
        command += b"e"
        command += bytes([position])
        command += b"\n"
        # newline indicates end of command to arduino
        self.send(command)

    def servo_state(self, state: str):
        if state == "right":
            self.servo(80-30)
        elif state == "left":
            self.servo(80+31)
        elif state == "centre":
            self.servo(80)

    def pulley(self, state: str):
        if state == "up":
            self.motor(75, "pulley")  # placeholder power
        elif state == "down":
            self.motor(-50, "pulley")
        elif state == "stop":
            self.motor(0, "pulley")

    def pulley_activate(self):
        """Time ration for up/down is approx 1.4"""
        self.pulley("up")
        time.sleep(5*0.7)  # placeholder time for rising pulley
        self.pulley("stop")
        time.sleep(2)
        self.pulley("down")
        time.sleep(5*0.5)
        self.pulley("stop")


    def pusher(self, state: str):
        if state == "push":
            self.motor(100, "pusher")  # placeholder power
        elif state == "retract":
            self.motor(-70, "pusher")
        elif state == "stop":
            self.motor(0, "pusher")

    def pusher_activate(self):
        self.pusher("push")
        time.sleep(2.15)   #Definitely not above 3.2!!!
        self.pusher("retract")
        time.sleep(3.2)
        self.pusher("stop")


    def offload(self):
        self.pulley("down")
        time.sleep(0.77)
        self.pulley("stop")# placeholder time for rising pulley
        self.pusher_activate()

        self.pulley("up")
        time.sleep(1.2)
        self.pulley_activate()

    """Request for sensor info"""

    def hall_effect(self):
        """request hall effect info"""
        self.serial.reset_input_buffer()  # clear buffer
        self.send(b"jj\n")
        #  next line depends on read timeout
        result = self.serial.read(1)
        if result == b'':
            print("no hall effect data returned")
            return 2  # if 2 returned do it again
        else:
            result = int.from_bytes(result, "big")
            return result

    def IR_sensor(self):
        """request hall effect info"""
        self.serial.reset_input_buffer()  # clear buffer
        self.send(b"kk\n")
        #  next line depends on read timeout
        result = self.serial.read(1)
        if result == b'':
            print("no IR data returned")
            return 2  # if 2 returned do it again
        else:
            result = int.from_bytes(result, "big")
            return result