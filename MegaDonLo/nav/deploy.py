from nav.Robot.Robot import Robot
from nav.Teleop.Teleop import Teleop
from nav.Autonomous.Autonomous import Autonomous
# SANNIE IMPORTS:
# from MegaDonLo.nav.Robot.Robot import Robot
# from MegaDonLo.nav.Teleop.Teleop import Teleop
# from MegaDonLo.nav.Autonomous.Autonomous import Autonomous

import multiprocessing

'''
    Initializes and creates Robot, Teleop object, begins teleop loop
'''

def run(queue_in, queue_out, testing_queue):
    rob = Robot (queue_in, queue_out, testing_queue)
    print("Robot initialized")
    teleop = Teleop(rob)
    print("teleop initialized")
    auto = Autonomous(rob, testing_queue)
    print("autonomous initialized")

    print("Robot, Teleop, and Autonomous Objects Initialized")

    ''' 
        loop checks whether or not to run teleop, autonomous docking, autonomous transect line, or none 
        there needs to be a conditional in teleop and autonomous that ends their loops 
        if the mode changes (queue_array[0] changes)
    '''
    while queue_in.empty():          # if there's nothing in the queue
        pass                         # wait
    loop = True
    while loop:
        # while queue_in.empty():          # if there's nothing in the queue
        #     pass                         # wait
        # queue_array = queue_in.get()     # until there is something
        queue_array = rob.get_queue()
        # print("deploy.py: " + str(queue_array))
        if queue_array[0] != 0:
            if queue_array[0] == 4:
                loop = False
                rob.queue_out.put([4, 0, 0, 0, 0, 0, 0])
                print("nav process ended")
            if queue_array[0] == 1:
                print("starting teleop")
                teleop.teleop_loop()
            # the autonomous object checks which autonomous task is being completed
            elif queue_array[0] == 2 or queue_array[0] == 3:
                print("starting autonomous")
                auto.begin_and_loop()


if __name__ == '__main__':
    run(1, 1, 1)