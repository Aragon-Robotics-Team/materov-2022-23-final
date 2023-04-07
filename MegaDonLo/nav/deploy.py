from nav.Robot.Robot import Robot
from nav.Teleop.Teleop import Teleop
from nav.Autonomous.Autonomous import Autonomous

import multiprocessing

'''
Initializes and creates Robot, Teleop object, begins teleop loop
'''

def run(queue_in, queue_out, testing_queue):
    rob = Robot (queue_in, queue_out, testing_queue)
    print("Robot initialized")
    teleop = Teleop(rob)
    print("teleop initialized")
    auto = Autonomous(rob)
    print("autonomous initialized")

    print("Robot, Teleop, and Autonomous Objects Initialized")

    #loop checks whether or not to run teleop, autonomous docking, autonomous transect line, or none 
    #there needs to be a conditional in teleop and autonomous that ends their loops if the mode changes (queue_array[0] changes)
    loop = True
    queue_array = [0, 0, 0]
    while loop:
        while queue_in.empty() == False:
            queue_array = queue_in.get()
        if queue_array[0] != 0:
            if queue_array[0] == 4: 
                loop = False
                print("nav process ended")
            if queue_array[0] == 1:
                print("starting teleop")
                teleop.teleop_loop()
            if queue_array[0] == 2:
                auto.begin_and_loop()
            #the autonomous object checks which autonomous task is being completed 
            # elif queue_array[0] == 2 or queue_array[0] == 3:
            #     auto.begin_and_loop()


if __name__ == '__main__':
    run(1, 1)