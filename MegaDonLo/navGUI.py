#Contains the methods that the GUI needs to call for nav purposes

import multiprocessing 
import imp

import nav.deploy

from imageProcessing.AutonomousDocking.AutonomousDocking import autodockingloop

from nav.Autonomous.Autonomous import Autonomous
from nav.Robot.Robot import Robot 


navOn = False

class NavProcess(multiprocessing.Process):
    def __init__(self, gui_nav, nav_gui, testing_queue):
        multiprocessing.Process.__init__(self)
        self.gui_nav = gui_nav
        self.nav_gui = nav_gui
        self.testing_queue = testing_queue
    def run(self): 
        nav.deploy.run(self.gui_nav, self.nav_gui, self.testing_queue)
        return 

def start_nav_process(gui_nav, nav_gui, testing_queue):
    global p
    global navOn
    navOn = True
    p = NavProcess(gui_nav, nav_gui, testing_queue)
    imp.reload(nav.deploy)
    p.start()

def terminate_nav_process(gui_nav):
    global navOn
    navOn = False
    gui_nav.put([4, 0, 0])
    # global p
    # p.terminate()

def start_teleop(gui_obj, gui_nav):
    global navOn
    if navOn == True:
        gui_obj.mode = "teleop"
        gui_nav.put([1, 0, 0])
    else:
        print("nav process is not active")

def start_autonomous_docking(gui_obj, gui_nav):
    global navOn
    if navOn == True:
        gui_obj.mode = "autonomous docking"
        autodockingloop(gui_obj.cap, gui_nav)

def testing_auto():
    queue = multiprocessing.Queue()
    rob = Robot (queue, queue, queue)
    auto = Autonomous(rob, queue)
    print(auto.autoDocking(100, 100))
    print(auto.autoDocking(500, 500))
    print(auto.autoDocking(1000, 1000))
    print(auto.autoDocking(1500, 1500))



