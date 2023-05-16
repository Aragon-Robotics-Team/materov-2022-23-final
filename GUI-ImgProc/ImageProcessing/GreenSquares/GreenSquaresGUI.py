import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import time
import keyboard
import tkinter as tk
import tkinter as tk
from .GreenSquares import HSVColorPicker
from .GreenSquares import square1
from .GreenSquares import square2
from .GreenSquares import calculator
from .GreenSquares import snapshots

import globalvars

#instructions:
#After running, press s to take a photo, when both photos are taken, press q
#Use the mouse to pick the correct colors when they pop up. Usually, the first photo has better thresholding with greens on the top 
#Press q after choosing a color so that the next image will pop up
#second photo has better thresholding with greens on the bottom right
#Press q after picking the second color
#Check console for print statement
#Exit masking window 

#---------------------
def runGreenSquares(downcamera, facetimecamera):
    flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

    result = True
    # videoCaptureObject = cv2.VideoCapture(1)

    i = 0
    while i == 0:
        ret,frame = downcamera.read()
        cv2.imshow("Bottom Camera Feed", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):    
            cv2.imwrite(snapshots[i], frame)
            cv2.imshow(snapshots[i], frame)
            i+= 1
    while i == 1: 
        ret,frame = facetimecamera.read()
        cv2.imshow("Facetime Camera Feed", frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(snapshots[i], frame)
            cv2.imshow(snapshots[i], frame)
            i+= 1

    # while True:
    #     ret, frame = videoCaptureObject.read()
    #     cv2.imshow("Capturing Video", frame)
    #         # deletes every frame as the next one comes on, closes all windows when q is pressed
    #     if cv2.waitKey(1) == ord('q'):
    #         videoCaptureObject.release()
    #         cv2.destroyAllWindows()
    #         break
    #         # when s is pressed
    #     if keyboard.is_pressed('s'):
    #             # and the index is less than txhe length of the snapshot list
    #         if i < 2:
    #                 # take as snapshot, save it, show it
    #             cv2.imwrite(snapshots[i], frame)
    #             cv2.imshow(snapshots[i], frame)
    #             time.sleep(1)
    #             i += 1
    #         else:
    #             result = False

    # image = cv2.imread("C:/Users/alexa/Desktop/square0.png")
    image = cv2.imread(globalvars.snapshots[0])
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    count = square1(HSVColorPicker(globalvars.snapshots[0]))
    countAfter = square2(HSVColorPicker(globalvars.snapshots[1]))

    print(calculator(count, countAfter))

# root = tk.Tk()
# run = tk.Button(text="Green Squares", command=runGreenSquares).pack()

# root.mainloop()