import cv2
import numpy as np
import argparse
import math

def findAngle(videoImg, B, G, R): 
    global image
    image = videoImg
    #gray_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array((B - 15,G - 15,R - 25), dtype = "uint8")
    upper = np.array((B + 15, G + 15, R + 25), dtype = "uint8")
    blurImg = cv2.blur(image,(10,10)) 
    mask = cv2.inRange(blurImg, lower, upper)
    #cv2.imshow("mask", mask)
    output = cv2.bitwise_and(image, image, mask = mask)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    cv2.imshow("result", output)
    #cv2.waitKey()
    edges = cv2.Canny(output, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength = 100, maxLineGap = 20)
    #cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) ---may be used? hmm test

    i = 0
    rightLinePresent = False

    if lines is not None:
        for line in lines:
            if i == 0:
                leftx1, lefty1, leftx2, lefty2 = line[0]
            else:
                rightx1, righty1, rightx2, righty2 = line[0]
                if abs(rightx1 - leftx1) > 90:
                    rightLinePresent = True
                    if (rightx1 - leftx1) < 0: 
                        rightx1 = leftx1
                        rightx2 = leftx2
                        righty1 = lefty1
                        righty2 = lefty2
                        leftx1, lefty1, leftx2, lefty2 = line[0]
                    if lefty1 > lefty2:
                        leftEndX = leftx1
                        leftStartX = leftx2
                    else:
                        leftEndX = leftx2
                        leftStartX = leftx1
                break
            i += 1

        if rightLinePresent:
            cv2.line(image, (leftx1, lefty1), (leftx2, lefty2), (0, 255, 255), 10)
            cv2.line(image, (rightx1, righty1), (rightx2, righty2), (255, 255, 255), 10)
            straightLFPWMOutput(leftEndX, leftStartX, lefty1, lefty2, videoImg)

def straightLFPWMOutput(x1, x2, y1, y2, videoImg):
    yComponent = abs(y1-y2) 
    xComponent = x1-x2
    if x1-x2 > 0:
        angleToAdjust = -1*(math.acos(yComponent/(math.sqrt(xComponent**2 + yComponent**2))))*180/math.pi
    else:
        angleToAdjust = (math.acos(yComponent/(math.sqrt(xComponent**2 + yComponent**2))))*180/math.pi
    print(angleToAdjust)
    #NAV CODE TO ADJUST ANGLE
    #lineMidpoint = (int)((x1+x2)/2)
    #imageMidpoint = (int)(videoImg.shape[1])
    #if lineMidpoint > imageMidpoint:
        #NAV CODE TO MOVE LEFT/RIGHT
    return(xComponent, yComponent)

def colorSelector(img):
	color_selected = np.zeros((150,150,3), np.uint8)

	global Bnum
	global Gnum
	global Rnum 

	Bnum = 0 
	Gnum = 0
	Rnum = 0

	#Mouse Callback function
	def show_color(event,x,y,flags,param): 
		global Bnum
		global Gnum
		global Rnum 
		B=img[y,x][0]
		G=img[y,x][1]
		R=img[y,x][2]

		if event == cv2.EVENT_LBUTTONDOWN:
			color_selected [:] = (B,G,R)
			Bnum = B
			Gnum = G
			Rnum = R

	#Show selected color when left mouse button pressed
	cv2.namedWindow('color_selected')
	cv2.resizeWindow("color_selected", 50,50);

	#image window for sample image
	cv2.namedWindow('image')

	#mouse call back function declaration
	cv2.setMouseCallback('image', show_color)
	while (1):
		cv2.imshow('image', img)
		cv2.imshow('color_selected', color_selected)
		if cv2.waitKey(1) == ord('q'):
			cv2.destroyAllWindows()
			break

	print("B: " + str(Bnum))
	print("G: " + str(Gnum))
	print("R: " + str(Rnum))
	return (Bnum, Gnum, Rnum)
