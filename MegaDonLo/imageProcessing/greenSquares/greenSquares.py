
import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
import time
import keyboard
import tkinter as tk

snapshots = ["C:/Users/alexa/Desktop/square0.png", "C:/Users/alexa/Desktop/square1.png"]

image_hsv = None

# root = tk.Tk()

#------------------------------
def HSVColorPicker(img_path):

	image = cv2.imread(img_path)
	image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	image_hsv = cv2.blur(image_hsv, (5,5))

	color_selected = np.zeros((150,150,3), np.uint8)

	global Bnum
	global Gnum
	global Rnum 

	Bnum = 0 
	Gnum = 0
	Rnum = 0

	#Mouse Callback function
	def show_color(event,x,y,flags,param): 
		global Hnum
		global Snum
		global Vnum 
		H=image_hsv[y,x][0]
		S=image_hsv[y,x][1]
		V=image_hsv[y,x][2]

		if event == cv2.EVENT_LBUTTONDOWN:
			color_selected [:] = (H,S,V)
			Hnum = H
			Snum = S
			Vnum = V

	#Show selected color when left mouse button pressed
	cv2.namedWindow('color_selected')
	cv2.resizeWindow("color_selected", 50,50)

	#image window for sample image
	cv2.namedWindow('image')

	#read sample image
	# img=cv2.imread(img_path)

	#mouse call back function declaration
	cv2.setMouseCallback('image',show_color)
	while (1):
		cv2.imshow('image',image_hsv)
		cv2.imshow('color_selected', color_selected)
		if cv2.waitKey(1) == ord('q'):
			cv2.destroyAllWindows()
			break

	return (Hnum, Snum, Vnum)

#---------------------------------
def square1(colors):

	H, S, V = colors

	lowerb = (H - 7, S - 55, V - 60)	
	upperb = (H + 7, S + 55, V + 60)

	lowerb = np.mat(lowerb)
	upperb = np.mat(upperb)
	

	#count squares

	squareOne = cv2.imread(snapshots[0])
	squareOne = cv2.GaussianBlur(squareOne, (5,5), 0)
	hsv_squareOne = cv2.cvtColor(squareOne, cv2.COLOR_RGB2HSV)


	mask = cv2.inRange(hsv_squareOne, lowerb, upperb)
	result = cv2.bitwise_and(squareOne, squareOne, mask=mask)

	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	count = 0
		
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 200):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(mask, (x,y), (x+w, y+h), (0,255,0), 2)
			cv2.putText(imageFrame, "Green", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
			count += 1
	
	cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
	cv2.waitKey(0)

	return count

#------------------------------------
def square2(colors):

	H, S, V = colors

	lowerb = (H - 5, S - 40, V - 40)	
	upperb = (H + 5, S + 40, V + 40)

	lowerb = np.mat(lowerb)
	upperb = np.mat(upperb)

	squareTwo = cv2.imread(snapshots[1])
	squareTwo = cv2.GaussianBlur(squareTwo, (5,5), 0)
	hsv_squareTwo = cv2.cvtColor(squareTwo, cv2.COLOR_RGB2HSV)

	mask = cv2.inRange(hsv_squareTwo, lowerb, upperb)
	result = cv2.bitwise_and(squareTwo, squareTwo, mask=mask)

	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	countAfter = 0
		
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 200):
			x, y, w, h = cv2.boundingRect(contour)
			imageFrame = cv2.rectangle(mask, (x,y), (x+w, y+h), (0,255,0), 2)
			cv2.putText(imageFrame, "Green", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
			countAfter += 1
	
	cv2.imshow("Second pic", imageFrame)
	cv2.waitKey(0)

	return countAfter
	
#-----------------------------------------	
def calculator(count, countAfter):

	print("countafter" + str(countAfter))
	print("count" + str(count))

	totalSquares = 64
	whiteAfter = totalSquares - countAfter
	whiteCount = totalSquares - count

	print("whiteafter" + str(whiteAfter))
	print("whitecount" + str(whiteCount))

	whiteDiff = whiteAfter - whiteCount
	greenDiff = countAfter - count

	if whiteDiff > greenDiff:
		return("The seagrass decreased by " + str(whiteDiff) + " white squares.")
	elif greenDiff > whiteDiff:
		return("The anchor tear recovered by " + str(greenDiff) + " green squares.")
	elif greenDiff == whiteDiff: 
		return("No change.")