import pygame
from nav.Teleop import MathFuncNew
from time import sleep
from nav.Teleop.Numbers import Numbers
from nav.Robot.Robot import Robot
# from nav.Autonomous import Autonomous

class Teleop:
    def __init__(self, rob: Robot) -> None:
        #### Pygame initialization
        pygame.init()
        pygame.joystick.init()
        pygame.display.init()
        while True:
            pygame.event.get()
            if pygame.joystick.get_count() > 0:
                break
        self.gamepad = pygame.joystick.Joystick(0)
        self.gamepad.init()
        self.controller_name = self.gamepad.get_name()
        print("Pygame initialized. Controller name:" + self.controller_name)

        self.numbers = Numbers()
        self.gamepad_states = [] # list you send to MathFunc
        self.robot = rob

    def teleop_loop(self):
        if self.controller_name == "Wireless Controller":
            self.var_ps4_controller()
        elif self.controller_name.find("XBOX") != -1:  # XBOX name?
            self.var_xbox_controller()
        else:
            self.var_big_controller()

        print("TELEOP STARTED")

        # ------ MATH CALC FUNCTION CALL ------ #
        while True:
            pygame.event.pump()
            gamepad_states = self.get_gamepad_states()
            message = self.thruster_calculations(gamepad_states)  # mathfunc
            self.robot.get_send_arduino(message)
            period = self.check_queue()
            if period != 0:  # if the queue is saying to exit teleop
                if period == 4:
                    #add command to stop the thrusters
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
        self.numbers.set_controller_vals([0, 1, 2, 3, 5, 8]) # buttons that are used TBD

    def var_ps4_controller(self):
        self.numbers.set_controller_vals([0, 1, 2, 6, 7]) 

    def thruster_calculations(self, gamepad_states) -> str:
        
        # gamepad_states = [shift x, shift y, yaw x, heave a, heave b]
        #variables here are for readability
        shift_x = self.gamepad_states[0]
        shift_y = self.gamepad_states[1]
        yaw_x = self.gamepad_states[2]
        heave_a = self.gamepad_states[3]
        heave_b = self.gamepad_states[4]
        
        # ------ MATH CALCS ------ #
        message = MathFuncNew.makeString(shift_x, shift_y, yaw_x, heave_a, heave_b, 100, 100)
        #  final SIX THRUSTER calculated values stored in "message" list ===>

        return message

    def get_gamepad_states(self) -> list:
        while True:
            all_states = []  # clearing the contents of the list with each loop iteration

            # get joystick axis values
            axes = self.gamepad.get_numaxes()
            for index in range(axes):
                axis = self.gamepad.get_axis(index)
                all_states.append(axis)
                
            # get joystick button values
            buttons = self.gamepad.get_numbuttons()
            for index in range(buttons):
                button = self.gamepad.get_button(index)
                all_states.append(button)

            # taking only the values that we need
            temp = [self.numbers.shift_x, self.numbers.shift_y, self.numbers.yaw_x, self.numbers.heave_a,
                    self.numbers.heave_b]
            print(temp)

            # for i in range(len(self.gamepad_states)):
            #     self.gamepad_states.append(all_states[temp[i]])
            #     print(self.gamepad_states)

            
            
            print(self.gamepad_states)

            return self.gamepad_states

    def check_queue(self):
        array = self.robot.get_queue()
        return array[0]
