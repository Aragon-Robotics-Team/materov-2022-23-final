from tkinter import *
from tkinter import ttk
from tkinter.simpledialog import askinteger, askstring

import cv2
from PIL import Image, ImageTk 
import globalvars

from ImageProcessing.GreenSquares.GreenSquaresGUI import runGreenSquares

from ImageProcessing.Photogrammetry.photoexif import takeVideo

from ImageProcessing.Photogrammetry.openModel import openModel

#----------------------------------------------------------------------------------------------------
#Returns a snapshot of the video feed the moment the function is called 
def snapshot(self, cap):
    cv2.imwrite(globalvars.generalsnapshot, cap.read()[1])
    return(globalvars.generalsnapshot) 

#----------------------------------------------------------------------------------------------------
#Checks whether the camera instances are the front camera, claw camera, or down camera 
def checkCameras(self):
    cv2.imshow("camera 1", self.cap.read()[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    camera1 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
    assignCamera(self, self.cap, camera1)
    if self.cap2 != None:
    # if cv2.VideoCapture(1).isOpened():
        cv2.imshow("camera 2", self.cap2.read()[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        camera2 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
        assignCamera(self, self.cap2, camera2)
    # if cv2.VideoCapture(2).isOpened():
    if self.cap3 != None:
        cv2.imshow("camera 3", self.cap3.read()[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        camera3 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
        assignCamera(self, self.cap3, camera3)
    if self.cap4 != None:
    # if cv2.VideoCapture(3).isOpened():
        cv2.imshow("camera 4", self.cap4.read()[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        camera4 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
        assignCamera(self, self.cap4, camera4)
    # if cv2.VideoCapture(4).isOpened():
    # if self.cap5 != None: 
    #     cv2.imshow("camera 5", self.cap5.read()[1])
    #     cv2.waitKey(0)
    #     camera5 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
    #     assignCamera(self, self.cap5, camera5)


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
    if gui_obj.downcamera is None: 
        print("bottom camera not initialized. Please click the assign cameras button to do so")
    elif gui_obj.facetimecamera is None:
        print("facetime camera not initialized. Please click the assign cameras button to do so")
    else:
        runGreenSquares(gui_obj.downcamera, gui_obj.facetimecamera)

#-------------------------------------------------------------------------------------

def startPhotogrammetryVideo(gui_obj):
    if gui_obj.frontcamera is None:
        print("front camera not initialized. Please click the assign cameras button to do so")
    else:
        takeVideo(gui_obj.frontcamera)

def manualModel():
    diameter = askinteger("Diameter","What is the diameter?")
    height = askinteger("Diameter", "What is the height?")
    openModel("/Users/valeriefan/Downloads/Magnificent Blad/tinker.obj", diameter, height)

def photogrammetryModel():
    filePath = askstring("filePath", "What is the filePath?")
    diameter = askinteger("Diameter","What is the diameter?")
    height = askinteger("Diameter", "What is the height?")
    openModel(filePath, diameter, height)
