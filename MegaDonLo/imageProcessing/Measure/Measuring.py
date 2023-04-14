import cv2
import threading
import math
import queue
import time
import sys
import os
import tkinter as tk
import numpy as np
import tkinter.font as font
from tkinter import messagebox, RIGHT, LEFT, StringVar
from time import sleep
import argparse

bowlCoords = [[0,0],[0,0], [0,0], [0,0]]
#[laserX1, laserY1],
#[laserX2, laserY2],
#[bowlX1, bowlY1],
#[bowlX2, bowlY2]
measurebowlieClick = False
#measurebowlieStart = False
measurebowlieCalc = False
countbowlCoords = 0
bowlImg = ""

bowlPictureCount = 0
allbowlLengths = [0,0,0]

def click_event(event, x, y, flags, params):
    global image
    global countbowlCoords
    global measurebowlieClick
    # checking for left mouse clicks for laser points
    if measurebowlieClick==True:
        if bowlPictureCount < 2:
            #print("click event")
            #print("MeasurebowlieClick is true in click event")
            if countbowlCoords < 4:
                if event == cv2.EVENT_LBUTTONDOWN:
                    #print("Button is clicked is true in click event")
                    # displaying the coordinates on the Shell
                    bowlCoords[countbowlCoords][0] = x
                    bowlCoords[countbowlCoords][1] = y
                    countbowlCoords = countbowlCoords + 1
                    # xcoords[countbowlCoords-1] = x
                    # ycoords[countbowlCoords-1] = y
                    print(x, ' ', y)

                    # displaying the coordinates
                    # on the image window
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(bowlImg, str(x) + ',' +
                                str(y), (x,y), font,
                                1, (255, 0, 0), 2)
                    #q.put(bowlImg)
                    cv2.imshow('bowl', bowlImg)
                    #countbowlCoords = countbowlCoords + 1
            else:
                measurebowlieClick = False
                #print("starting bowl calculations")
                measurebowlieCalculations()
                cv2.destroyAllWindows()

def measurebowlieCalculations():
    global bowlPictureCount
    global countbowlCoords
    global measurebowlieClick
    global bowlCoords

    #finding distances
    laserPixels = math.sqrt(((bowlCoords[0][0]-bowlCoords[1][0])**2) + ((bowlCoords[0][1]-bowlCoords[1][1]) **2))
    print("Laser Pixels per cm: " + str(laserPixels))
    bowlPixels = math.sqrt(((bowlCoords[2][0]-bowlCoords[3][0])**2) + ((bowlCoords[2][1]-bowlCoords[3][1]) **2))
    print("Total bowl Pixels: " + str(bowlPixels))
    bowlLength = bowlPixels / laserPixels
    print("bowl Length in cm: " + str(bowlLength))
    allbowlLengths[bowlPictureCount] = bowlLength
    bowlPictureCount = bowlPictureCount + 1

def measurebowlie():
    #reset variables for new image
    global countbowlCoords
    global measurebowlieClick
    global bowlCoords
    global bowlImg
    countbowlCoords = 0
    measurebowlieClick = True

    if bowlPictureCount < 2:
        #show image and read coordinates
        print("bowl #: " + str(bowlPictureCount + 1))
        ret, frame = videoCaptureObject.read()
        bowlImg = frame
        cv2.imshow("bowl", bowlImg)
        cv2.setMouseCallback("bowl", click_event)
    else:
        print("Bowl Diameter: " + str(allbowlLengths[0]))
        print("Bowl Height: " + str(allbowlLengths[1]))


# Bu = tk.Button(root, text="Measure bowl", command = measurebowlie).pack()

def resetMeasurebowl():
    print("Measuring bowl Task Reset")
    global allbowlLengths
    global bowlPictureCount
    global countbowlCoords
    allbowlLengths = [0,0,0]
    countbowlCoords = 0
    bowlPictureCount = 0

# Bu = tk.Button(root, text="Reset bowl Measuring", command = resetMeasurebowl).pack()


#DON"T NEED TO CHANGE WHEN ADDED INTO THE MAIN PROGRAM
videoCaptureObject = cv2.VideoCapture(0)
photomosaicCount = 0
#BM: Video Feed
def videoCapture():
    global photomosaicVideo
    global photomosaicStart
    global photomosaicCount
    ret, frame = videoCaptureObject.read()
    cv2.imshow("Capturing Video", frame)
    # deletes every frame as the next one comes on, closes all windows when q is pressed
    if cv2.waitKey(1) == ord('q'):
        videoCaptureObject.release()
        cv2.destroyAllWindows()

#TODO: Add equation to calculate average length, then average mass of the  cohort of bowl
#Integrate into main program

# while True:
#     #queue()
#     videoCapture()
#     root.update()
