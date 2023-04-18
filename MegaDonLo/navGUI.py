

##
##Contains the methods that the GUI needs to call for nav purposes
##

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
    gui_nav.put([4, 0, 0]) #turn off the thrusters and end the nav loop  
    # global p
    # p.terminate()

def start_teleop(gui_obj, gui_nav):
    global navOn
    if navOn == True: #if the nav process has started 
        gui_obj.mode = "teleop"
        gui_nav.put([1, 0, 0]) #start teleop 
    else:
        print("nav process is not active") #else, don't start teleop 

def start_autonomous_docking(gui_obj, gui_nav):
    global navOn
    if gui_obj.frontcamera.isOpened():
        if navOn == True:
            gui_obj.mode = "autonomous docking"
            autodockingloop(gui_obj.frontcamera, gui_nav) #runs the image processing autonomous docking loop 
    else:
        print("front camera not initialized. Please click the assign cameras button to do so")

def end_autonomous(gui_nav):
    gui_nav.put([1, 0 ,0]) #changes to teleop 