#---------------------------------------
#basic gui imports
from tkinter import *
from tkinter import ttk

#multiprocessing
import multiprocessing
import navGUI

class GUIClass():
    def __init__(self):
        #basic setup 
        self.root = Tk()
        self.root.geometry("1300x1000")

        #styling
        self.style =  ttk.Style()
        self.style.theme_create( "button-center", parent="alt", settings={"TButton": {"configure": {"anchor": "center"}}} )
        self.style.configure('TButton', font = ('Helvetica', 13), width = 25)
        self.vcol = 3 #number of columns that the video feed, or else the video is weirdly squished for some reason 
        self.vrow = 40 #number of rows that the video feed needs to span, same reasoning as above 

        #multiprocessing
        self.gui_nav = multiprocessing.Queue()
        self.nav_gui = multiprocessing.Queue() 

        start_nav_b = Button(self.root, text = "Begin Nav Process", command = lambda: navGUI.start_nav_process(self.gui_nav, self.nav_gui))
        start_nav_b.grid(row = 0, column = self.vcol + 1, sticky = 'n')

        end_nav_b = Button(self.root, text = "Terminate Nav Process", command = lambda: navGUI.terminate_nav_process(self.gui_nav))
        end_nav_b.grid(row = 1, column = self.vcol + 1, sticky = 'n')

        #navigation 
        self.mode = "none"

        start_teleop = Button(self.root, text = "Teleop", command = lambda: navGUI.start_teleop(self, self.gui_nav))
        start_teleop.grid(row = 2, column = self.vcol + 1, sticky = 'n')

            #insert button to start teleop 
            #insert button to start autonomous 

        #insert Button/Label 

    def run(self):
        while True:
            self.root.update()
        
    # def queueRecieve():

if __name__ == "__main__":
    gui = GUIClass()
    gui.run()

