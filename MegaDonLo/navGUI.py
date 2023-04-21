

##
##Contains the methods that the GUI needs to call for nav purposes
##

import multiprocessing 
import imp

import nav.deploy

from ImageProcessing.AutonomousDocking.AutonomousDocking import autodockingloop
from ImageProcessing.AutonomousDocking.AutonomousDocking import autodockinit


from nav.Autonomous.Autonomous import Autonomous
from nav.Robot.Robot import Robot 

from ImageProcessing.TransectLine.TransectButton import startTransect

import guiFuncs


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
    gui_nav.put([0, 0, 0])
    nav_gui.put([0, 0, 0, 0, 0, 0, 0])

def terminate_nav_process(gui_nav, nav_gui):
    global navOn
    navOn = False 
    gui_nav.put([4, 0, 0]) #turn off the thrusters and end the nav loop  
    # nav_gui.put([4, 0, 0, 0, 0, 0, 0])
    # global p
    # p.terminate()

def start_teleop(gui_obj, gui_nav):
    global navOn
    if navOn == True: #if the nav process has started 
        gui_nav.put([1, 0, 0]) #start teleop 
    else:
        print("nav process is not active") #else, don't start teleop 

def autonomous_docking_init(gui_obj):
    global navOn
    if gui_obj.frontcamera is None: 
        print("front camera not initialized. Please click the assign cameras button to do so")
    else: 
        if navOn == True:
            autodockinit(guiFuncs.snapshot(gui_obj, gui_obj.frontcamera))
            

def start_autonomous_docking(gui_obj, gui_nav):
    global navOn
    if gui_obj.frontcamera is None: 
        print("front camera not initialized. Please click the assign cameras button to do so")
    else: 
        if navOn == True:
            gui_obj.mode = "autonomous docking"
            autodockingloop(gui_obj.frontcamera, gui_nav) #runs the image processing autonomous docking loop 

def end_autonomous(gui_nav):
<<<<<<< Updated upstream
    gui_nav.put([1, 0 ,0]) #changes to teleop 

def start_autonomous_transect(gui_obj, gui_nav):
    global navOn
    if gui_obj.downcamera is None:
        print("bottom camera not initialized. Please click the assign cameras button to do so")
    else:
        if navOn == True:
            startTransect(gui_obj.downcamera, gui_nav)
=======
    gui_nav.put([1, 0 ,0])


# BELOW IS EMERGENCY STOP AND START FUNCTION - ADD URSELF
def enableBot():
    global autoArray
    autoArray[1] = 0
    output_queue.put(autoArray)
    print ("BOT ENABLED")

def disableBot():
    global autoArray
    autoArray[1] = 1
    output_queue.put(autoArray)
    print("BOT DISABLED")

# def testing_auto():
#     queue = multiprocessing.Queue()
#     rob = Robot (queue, queue, queue)
#     auto = Autonomous(rob, queue)
#     print(auto.autoDocking(100, 100))
#     print(auto.autoDocking(500, 500))
#     print(auto.autoDocking(1000, 1000))
#     print(auto.autoDocking(1500, 1500))

>>>>>>> Stashed changes
