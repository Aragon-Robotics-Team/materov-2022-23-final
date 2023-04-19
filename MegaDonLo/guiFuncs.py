from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askinteger

import cv2
from PIL import Image, ImageTk 
import globalvars

from ImageProcessing.GreenSquares.GreenSquaresGUI import runGreenSquares

#----------------------------------------------------------------------------------------------------
#Repeating loop that updates the video frame on the GUI (i.e. shows the video feed)
def showFrames(self):
    # self.camerafeedpath = "/Users/valeriefan/Desktop/MATE ROV 2023 /camerafeed.jpg"
    self.camerafeedpath = globalvars.camerafeedpath
    cv2.imwrite(self.camerafeedpath, self.cap.read()[1])

    cv2image= cv2.cvtColor(cv2.imread(self.camerafeedpath) ,cv2.COLOR_BGR2RGB)
    # cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
    #error is fine 
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    #error is fine
    self.videolabel.imgtk = imgtk
    self.videolabel.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    self.videolabel.after(20, lambda: showFrames(self))

#----------------------------------------------------------------------------------------------------
#Returns a snapshot of the video feed the moment the function is called 
def snapshot(self, cap):
    cv2.imwrite(globalvars.generalsnapshot, cap.read()[1])
    return(globalvars.generalsnapshot) 

#----------------------------------------------------------------------------------------------------
#Repeating loop that sends the slider values through the queue 
def send_testing_queue(self):
    #send through queue
    self.coeffs = [self.autodocking_slider.get(), self.autoline_slider.get(), self.vmax_val.get(), self.lmax_val.get(), self.pmax_val.get()]
    # print(self.coeffs)
    self.testing_queue.put(self.coeffs)

    #loop every 20 ms
    self.root.after(20, lambda: send_testing_queue(self))

#----------------------------------------------------------------------------------------------------
#Checks whether the camera instances are the front camera, claw camera, or down camera 
def checkCameras(self):
    cv2.imshow("camera 1", self.cap.read()[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    camera1 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime", "Which camera view is this?")
    assignCamera(self, self.cap, camera1)
    if cv2.VideoCapture(1).isOpened():
        cv2.imshow("camera 2", self.cap2.read()[1])
        cv2.waitKey(0)
        camera2 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
        self.assignCamera(self.cap2, camera2)
    if cv2.VideoCapture(2).isOpened():
        cv2.imshow("camera 3", self.cap3.read()[1])
        cv2.waitKey(0)
        camera3 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
        assignCamera(self, self.cap3, camera3)
    if cv2.VideoCapture(3).isOpened():
        cv2.imshow("camera 4", self.cap4.read()[1])
        cv2.waitKey(0)
        camera4 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
        assignCamera(self, self.cap4, camera4)
    

def assignCamera(self, cap, answer):
    if answer == 1:
        self.frontcamera = cap
        print("assigned to front camera")
    elif answer == 2:
        self.clawcamera = cap
        print("assigned to claw camera")
    elif answer == 3:
        self.downcamera = cap
        print("assigned to down camera")
    elif answer == 4:
        self.facetimecamera = cap
        print("assigned to facetime camera")

#----------------------------------------------------------------------------------------------------

def startGreenSquares(gui_obj):
    if gui_obj.frontcamera is None: 
        print("front camera not initialized. Please click the assign cameras button to do so")
    elif gui_obj.facetimecamera is None:
        print("facetime camera not initialized. Please click the assign cameras button to do so")
    else:
        runGreenSquares(gui_obj.frontcamera, gui_obj.facetimecamera)


#----------------------------------------------------------------------------------------------------
#Displays whether or not the bot is in teleop, autonomous docking, or autonomous transect line 
def update_mode_label(self):
    queue_val = self.get_nav_gui_queue()
    # print('asdf')
    # print("nav_gui queue: " + str(queue_val))
    if queue_val[0] == 0:
        self.mode_label.config(text = "Mode: Nav Process Started ")
    elif queue_val[0] == 1:
        self.mode_label.config(text = "Mode: Teleop")
    elif queue_val[0] == 2:
        self.mode_label.config(text = "Mode: Auto Docking")
    elif queue_val[0] == 3:
        self.mode_label.config(text = "Mode: Auto Transect")
    elif queue_val[0] == 4:
        self.mode_label.config(text = "Mode: Nav Process Ended")
    elif queue_val[0] == 5:
        self.mode_label.config(text = "Mode: None")


    self.mode_label.after(20, lambda: update_mode_label(self))
