import cv2
import numpy as np
	

def colorSelector(img_path):
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

	#read sample image
	img=cv2.imread(img_path)

	#mouse call back function declaration
	cv2.setMouseCallback('image',show_color)
	while (1):
		cv2.imshow('image',img)
		cv2.imshow('color_selected', color_selected)
		if cv2.waitKey(1) == ord('q'):
			cv2.destroyAllWindows()
			break

	print("B: " + str(Bnum))
	print("G: " + str(Gnum))
	print("R: " + str(Rnum))
	return (Bnum, Gnum, Rnum)

# colorSelector("/Users/valeriefan/Desktop/reddot.png")
# print(colorSelector("/Users/valeriefan/Desktop/reddot.png"))
