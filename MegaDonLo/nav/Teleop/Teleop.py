import pygame
from time import sleep

from nav.Teleop import MathFunc
from nav.Teleop.Numbers import Numbers
from nav.Robot.Robot import Robot
from nav.Autonomous import Autonomous

# COMMENT OUT SANNIE IMPORTS:
#
# from MegaDonLo.nav.Teleop import MathFunc
# from MegaDonLo.nav.Teleop.Numbers import Numbers
# from MegaDonLo.nav.Robot.Robot import Robot
# from MegaDonLo.nav.Autonomous.Autonomous import Autonomous

class Teleop:
    def __init__(self, rob: Robot) -> None:
        #### Pygame initialization
        pygame.init()
        pygame.joystick.init()
        # pygame.display.init()
        # while True:
        #     pygame.event.get()
        #     print("Gamepad is disconnected")
        #     if pygame.joystick.get_count() > 0:
        #         break
        self.gamepad = pygame.joystick.Joystick(0)
        self.gamepad.init()
        self.controller_name = self.gamepad.get_name()
        print("Pygame initialized. Controller name:" + self.controller_name)

        self.numbers = Numbers()
        # self.gamepad_states = [] # list you send to MathFunc
        self.robot = rob

    def teleop_loop(self):
        gp_name = self.gamepad.get_name()
        if gp_name == "Wireless Controller":
            self.var_ps4_controller()
        elif gp_name.find("BOX") != -1:  # XBOX name?
            self.var_xbox_controller()
        else:
            self.var_big_controller()
        self.var_xbox_controller()
        print(gp_name, self.numbers.heave_b)

        print("TELEOP STARTED")

        # ------ MATH CALC FUNCTION CALL ------ #
        while True:
            pygame.event.pump()

            all_gp_states = self.get_gamepad_states()  # stores all the states of the gamepad into an array

            shift_x = all_gp_states[self.numbers.shift_x]  # calculates the states of the speecified things we need based on what controller we have
            shift_y = all_gp_states[self.numbers.shift_y]
            yaw_x = all_gp_states[self.numbers.yaw_x]
            heave_a = all_gp_states[self.numbers.heave_a]
            heave_b = all_gp_states[self.numbers.heave_b]
            # temporary straight forward/back to try with left stick

            # ------ MATH CALCS ------ #
            pwmArray = MathFunc.makeString(shift_x, shift_y, yaw_x, heave_a, heave_b, 90, 90, self.robot)

            # ------ TEMPORARY LEFT STICK STRAIGHT FORWARD/BACK CALCS ------ #
            drive_straight = all_gp_states[2] * -1

            if abs(drive_straight) > 0.1:  # deadband of 0.1 for left stick

                # drive straight function:
                ds_pwm = round(((abs(drive_straight) ** 1.5) * (drive_straight / abs(drive_straight)) * 350))

                pwmArray[0] += ds_pwm
                pwmArray[1] += ds_pwm
                pwmArray[2] += ds_pwm
                pwmArray[3] += ds_pwm

            # print(pwmArray)

            self.robot.get_send_arduino(pwmArray)

            queue_message = self.robot.get_queue()
            if len(queue_message) > 0:
                period = queue_message[0]
                if period != 0:  # if the queue is saying to exit teleop
                    if period == 4:
                        self.robot.get_send_arduino([1500,1500,1500,1500,1500,1500])
                        pass
                    break

            pygame.event.clear()
            sleep(self.robot.delay)
        # takes the message list (all the thruster values) and separates by comma and period
        # uses arduino function in Robot to send to arduino

    # note: array in [LX, LT, RX, A, B]
    def var_xbox_controller(self):
        #  EXAMPLE :D
        self.numbers.set_controller_vals([0, 1, 3, 6, 7])  # shift x, shift y, yaw x, heave a, heave b

    def var_big_controller(self):
        self.numbers.set_controller_vals([0, 1, 3, 5, 6])

    def var_ps4_controller(self):
        self.numbers.set_controller_vals([0, 1, 2, 6, 7]) 

    def get_gamepad_states(self) -> list:
        gp_states = []  # clear every iteration

        joystick_count = pygame.joystick.get_count()
        # For each interactable:
        for index in range(joystick_count):
            joystick = pygame.joystick.Joystick(index)
            joystick.init()

            # get joystick axis values
            axes = joystick.get_numaxes()
            for index in range(axes):
                axis = joystick.get_axis(index)
                gp_states.append(round(joystick.get_axis(index), 4))

            # get joystick button values
            buttons = joystick.get_numbuttons()
            for index in range(buttons):
                button = joystick.get_button(index)
                gp_states.append(button)

        return gp_states

    # def check_queue(self):
    #     obj = []
    #     while not self.robot.queue_out.empty():
    #         obj = self.robot.queue_out.get()

    #     return obj

