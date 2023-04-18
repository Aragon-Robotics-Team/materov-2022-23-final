import numpy as np 
import imutils
import cv2 
from .AutoDockingColorPicker import colorSelector
import multiprocessing 

B = 0
G = 0
R = 0

#--------------------------
def autodockinit(img_path):
    #find the color of the target in order to create a range for our mask in autodocking()
    global B, G, R
    B,G,R = colorSelector(img_path)

#---------------------------
def autodockingloop(cap, nav_queue):
    videocap = cap
    autodockingimgpath = "/Users/valeriefan/Desktop/MATE ROV 2023 /autodockingloop.jpg"
    #tracking the docking button in the live video feed 
    while (1): 
        cv2.imwrite(autodockingimgpath, videocap.read()[1])
        # cv2.imwrite(autodockingimgpath, cv2.imread(camerafeedpath))
        contours, cX, cY = autodocking(autodockingimgpath)
        cv2.imshow("Contours", contours)
        vY = cY - contours.shape[0]
        vX = cX - contours.shape[1]
        queueArray = [2, vX, vY]
        nav_queue.put(queueArray)
        # print(queueArray)
        #calculatethrust(cX, cY)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows
            print("autonomous docking ended")
            nav_queue.put([1, 0 ,0])
            break
        # cv2.waitKey(0)

#------------------------------------------

def calculateandsendthrust(cX, cY):
    #*insert calculations for thrust* 
    #*use queue to send to nav process* 
    return 

def autodocking(img_path): 
    #set the threshold for the mask, based on the color of the target  
    lower = np.array((B - 15,G - 15,R - 25), dtype = "uint8")
    upper = np.array((B + 15, G + 15, R + 25), dtype = "uint8")

    image = cv2.imread(img_path)
    if image is None:
        print("no image in path")

    #blur, mask and grayscale the image --- mask everything but the red circle 
    blurImg = cv2.blur(image,(10,10)) 
    mask = cv2.inRange(blurImg, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray", gray)
    # cv2.waitKey(0)

    #finding contours 
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    if len(cnts) != 0: 
        #grabs contours 
        cnts = imutils.grab_contours(cnts)
        #finds the largest contour 
        c = max(cnts, key=cv2.contourArea, default = 0 )

        #finding center of contours
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            #draw contours onto the original image 
            contours = image.copy()
            cv2.drawContours(contours, [c], -1, (0, 255, 0), 3)
            (x, y, w, h) = cv2.boundingRect(c)
            text = "original, num_pts={}".format(len(c))
            cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            #draw center of mass 
            cv2.circle(contours, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(contours, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # cv2.imshow("Original Contour", contours)
            
            #returns the modified image (with red circle marked), and the coordiantes of the red circle 
            return (contours, cX, cY)
        # cv2.waitKey(0)

    print("no contours ")
    return (image, 0, 0)