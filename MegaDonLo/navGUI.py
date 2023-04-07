#Contains the methods that the GUI needs to call for nav purposes

import multiprocessing 
import imp

import nav.deploy

from imageProcessing.AutonomousDocking.AutonomousDocking import autodockingloop

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

def start_autonomous_docking(gui_obj, gui_nav, camerafeedpath):
    global navOn
    if navOn == True:
        gui_obj.mode = "autonomous docking"
        autodockingloop(gui_obj.cap, gui_nav, camerafeedpath)
        
class AutonomousDocking(multiprocessing.Process):
    def __init__(self, gui_nav, nav_gui, testing_queue, camerafeedpath):
        multiprocessing.Process.__init__(self)
        self.gui_nav = gui_nav
        self.nav_gui = nav_gui
        self.testing_queue = testing_queue
        self.camerafeedpath = camerafeedpath
        # self.cap = cap
    def run(self): 
        autodockingloop(self.gui_nav, self.gui_nav.cap, self.camerafeedpath)
        return 
    
def start_autonomous_docking_p(gui_nav, nav_gui, testing_queue, gui_obj, camerafeedpath):
    global navOn
    if navOn == True:
        gui_obj.mode = "teleop"
        p = AutonomousDocking(gui_nav, nav_gui, testing_queue, camerafeedpath)
        p.start()
