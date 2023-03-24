#---------------------------------------
#basic gui imports
from tkinter import *
from tkinter import ttk

#multiprocessing
import multiprocessing
from MegadonLo2023.GUI.nav import navGUI


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
        self.nav_in_queue = multiprocessing.Queue()
        self.nav_out_queue = multiprocessing.Queue() 

        StartNavB = Button(self.root, text = "Start Nav Process", command = lambda: navGUI.startNavProcess(self.nav_in_queue, self.nav_out_queue))
        StartNavB.grid(row = 0, column = self.vcol + 1, sticky = 'n')

        EndNavB = Button(self.root, text = "Terminate Nav Process", command = navGUI.terminateNavProcess)
        EndNavB.grid(row = 1, column = self.vcol + 1, sticky = 'n')

        #insert Button/Label 

    def run(self):
        while True:
            self.root.update()

if __name__ == "__main__":
    gui = GUIClass()
    gui.run()

