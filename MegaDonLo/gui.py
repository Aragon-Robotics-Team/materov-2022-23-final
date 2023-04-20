#---------------------------------------
#basic gui imports
from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askinteger

#video feed
import cv2
from PIL import Image, ImageTk 

#multiprocessing
import multiprocessing
import navGUI

#measuring
from ImageProcessing.Measure.Measuring import measurebowlie, resetMeasurebowl

#GUI FUNCTIONS 
import guiFuncs


class GUIClass():
    def __init__(self):
        #basic setup 
        self.root = Tk()
        self.root.geometry("1300x1000")

        #styling
        self.style =  ttk.Style()
        self.style.theme_create( "button-center", parent="alt", settings={"TButton": {"configure": {"anchor": "center"}}} )
        self.style.configure('TButton', font = ('Helvetica', 13), width = 25)
        self.vcol = 1 #number of columns that the video feed, or else the video is weirdly squished for some reason 
        self.vrow = 1 #number of rows that the video feed needs to span, same reasoning as above 

        #video feed 
        self.cap = cv2.VideoCapture(0)
        if cv2.VideoCapture(1).isOpened():
            self.cap2 = cv2.VideoCapture(1)
            print("2")
        if cv2.VideoCapture(2).isOpened():
            self.cap3 = cv2.VideoCapture(2)
            print("3")
        if cv2.VideoCapture(3).isOpened():
            self.cap4 = cv2.VideoCapture(3)
            print("4")
        if cv2.VideoCapture(4).isOpened():
            self.cap5 = cv2.VideoCapture(4)
            print("5")

        # self.frontcamera = self.cap 
        # self.clawcamera = self.cap
        # self.downcamera = self.cap

        self.frontcamera = None 
        self.clawcamera = None
        self.downcamera = None
        

        # self.videolabel = Label(self.root, height = 800, width = 1000) ##CHANGE SO THE FULL VIDEO IS SHOWN 
        # self.videolabel.grid(row = 0, column = 0, rowspan = self.vrow, columnspan = self.vcol, sticky = 'n')

        #multiprocessing
        self.gui_nav = multiprocessing.Queue() 
            #Teleop: [1, 0, 0]
            #Autonomous Docking: [2, x, y]
            #Autonomous Transect Line: [3, x, y]
            #End Nav Process: [4, 0, 0]
        self.nav_gui = multiprocessing.Queue() 
            #[mode, rf, lf, rb, lb, v1, v2]
        self.nav_gui_val = [5, 0, 0, 0, 0, 0, 0]
            #holds the value of the nav_gui

        self.start_nav_b = Button(self.root, text = "Begin Nav Process", command = lambda: navGUI.start_nav_process(self.gui_nav, self.nav_gui, self.testing_queue))
        self.start_nav_b.grid(row = 0, column = self.vcol + 1, sticky = 'n')

        self.end_nav_b = Button(self.root, text = "Terminate Nav Process", command = lambda: navGUI.terminate_nav_process(self.gui_nav, self.nav_gui))
        self.end_nav_b.grid(row = 1, column = self.vcol + 1, sticky = 'n')

        #navigation 
        self.mode = "none"

        start_teleop = Button(self.root, text = "Teleop", command = lambda: navGUI.start_teleop(self, self.gui_nav))
        start_teleop.grid(row = 2, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking_init = Button(self.root, text = "Initialize Auto Docking", command = lambda: navGUI.autonomous_docking_init(self))
        self.autonomous_docking_init.grid(row = 3, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking = Button(self.root, text = "Auto Docking Live", command = lambda: navGUI.start_autonomous_docking(self, self.gui_nav))
        self.autonomous_docking.grid(row = 5, column = self.vcol + 1, sticky = 'n')

        self.end_autonomous = Button(self.root, text = "end autonomous", command = lambda: navGUI.end_autonomous(self.gui_nav))
        self.end_autonomous.grid(row = 6, column = self.vcol + 1, sticky = 'n')

        #autonomous testing 
        self.testing_queue = multiprocessing.Queue()
            #[Autodocking slider, Auto Transect Line Slider, Vertical Slider, Horizontal Slider, Pivot Slider]

        self.autodocking_val= DoubleVar(self.root, value = 5)
        self.autoline_val = DoubleVar(self.root, value = 5)

        Label(self.root, text = "_________________________________").grid(row = 7, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "Autonomous Docking Slider").grid(row = 8, column = self.vcol + 1, sticky = 'n')
        self.autodocking_slider = Scale(self.root, variable = self.autodocking_val, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        self.autodocking_slider.grid(row = 9, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 10, column = self.vcol + 1, sticky = 'n')

        Label(self.root, text = "Autonomous Transect Line Slider").grid(row = 11, column = self.vcol + 1, sticky = 'n')
        self.autoline_slider = Scale(self.root, variable = self.autoline_val, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        self.autoline_slider.grid(row = 12, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 13, column = self.vcol + 1, sticky = 'n')

        # self.autodocking_test = Button(self.root, text = "autodocking test", command = navGUI.testing_auto)
        # self.autodocking_test.grid(row = 12, column = self.vcol + 1, sticky = 'n')

        #Nav Mode 
        self.mode_label = Label(self.root, text = self.mode)
        self.mode_label.grid(row = 14, column = self.vcol + 1)

        #Nav Sliders 

        self.vmax_val = DoubleVar(self.root, value = 75)
        self.lmax_val = DoubleVar(self.root, value = 75)
        self.pmax_val = DoubleVar(self.root, value = 75)

        Label(self.root, text = "_________________________________").grid(row = 715, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "Vertical Max Slider").grid(row = 16, column = self.vcol + 1, sticky = 'n')
        self.vertical_max = Scale(self.root, variable = self.vmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.vertical_max.grid(row = 17, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 18, column = self.vcol + 1, sticky = 'n')

        Label(self.root, text = "Lateral Max Slider").grid(row = 20, column = self.vcol + 1, sticky = 'n')
        self.lateral_max = Scale(self.root, variable = self.lmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.lateral_max.grid(row = 21, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 22, column = self.vcol + 1, sticky = 'n')

        Label(self.root, text = "Pivot Max Slider").grid(row = 24, column = self.vcol + 1, sticky = 'n')
        self.pivot_max = Scale(self.root, variable = self.pmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.pivot_max.grid(row = 25, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 26, column = self.vcol + 1, sticky = 'n')
        
        #testing cameras 
        self.camera_testing = Button(self.root, text = "Assign Cameras", command = lambda: guiFuncs.checkCameras(self))
        self.camera_testing.grid(row = 27, column = self.vcol + 1, sticky = 'n')
        
        #green squares
        self.green_squares = Button(self.root, text = "Green Squares Program", command = lambda: guiFuncs.startGreenSquares(self))
        self.green_squares.grid(row = 28, column = self.vcol + 1, sticky = 'n')
        
        #measuring 
        self.measure = Button(self.root, text = "Measure bowl", command = measurebowlie)
        self.measure.grid(row = 29, column = self.vcol + 1, sticky = 'n' )

        self.reset_measure = Button(self.root, text = "Reset Measuring", command = resetMeasurebowl)
        self.reset_measure.grid(row = 30, column = self.vcol + 1, sticky = 'n')
        
        #transect line
        self.transect_line = Button(self.root, text = "Transect Line", command = lambda: navGUI.start_autonomous_transect(self, self.gui_nav))
        self.transect_line.grid(row = 31, column = self.vcol + 1, sticky = 'n')

        
        # #insert Button/Label 


    def get_nav_gui_queue(self):
        while self.nav_gui.empty() == False:
            self.nav_gui_val = self.nav_gui.get()

        # print("nav_gui_queue: " + str(self.nav_gui_val))
        return self.nav_gui_val


    def run(self):
        while True:
            self.root.update()

if __name__ == "__main__":
    gui = GUIClass()
    # gui.showFrames()
    guiFuncs.send_testing_queue(gui)
    guiFuncs.update_mode_label(gui)
    # guiFuncs.checkCameras(gui)
    gui.run()

