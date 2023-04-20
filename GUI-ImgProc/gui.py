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
        self.facetimecamera = None 
        

        #testing cameras 
        self.camera_testing = Button(self.root, text = "Assign Cameras", command = lambda: guiFuncs.checkCameras(self))
        self.camera_testing.grid(row = 1, column = self.vcol + 1, sticky = 'n')
        
        #green squares
        self.green_squares = Button(self.root, text = "Green Squares Program", command = lambda: guiFuncs.startGreenSquares(self))
        self.green_squares.grid(row = 2, column = self.vcol + 1, sticky = 'n')
        
        #measuring 
        self.measure = Button(self.root, text = "Measure bowl", command = measurebowlie)
        self.measure.grid(row = 3, column = self.vcol + 1, sticky = 'n' )

        self.reset_measure = Button(self.root, text = "Reset Measuring", command = resetMeasurebowl)
        self.reset_measure.grid(row = 4, column = self.vcol + 1, sticky = 'n')

        #photogrammetry video 
        self.photogrammetryVideo = Button(self.root, text = "Collect Photogrammetry Dataset", command = lambda: guiFuncs.startPhotogrammetryVideo(self))
        self.photogrammetryVideo.grid(row = 5, column = self.vcol + 1, sticky = 'n')

        
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
    gui.run()

