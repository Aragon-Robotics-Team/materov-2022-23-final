#Contains the methods that the GUI needs to call for nav purposes

import multiprocessing 
import imp

import nav.deploy

navOn = False

class NavProcess(multiprocessing.Process):
    def __init__(self, gui_nav, nav_gui):
        multiprocessing.Process.__init__(self)
        self.gui_nav = gui_nav
        self.nav_gui = nav_gui
    def run(self): 
        nav.deploy.run(self.gui_nav, self.nav_gui)
        return 

def start_nav_process(gui_nav, nav_gui):
    global p
    global navOn
    navOn = True
    p = NavProcess(gui_nav, nav_gui)
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

