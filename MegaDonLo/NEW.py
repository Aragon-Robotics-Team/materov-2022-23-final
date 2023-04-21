#---------------------------------------
#basic gui imports
from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
#video feed
import cv2 
import multiprocessing 
from PIL import Image, ImageTk 
#multiprocessing
import multiprocessing
import navGUI
#autonomous docking
from imageProcessing.AutonomousDocking.AutonomousDocking import autodockinit



class GUIClass():
    def __init__(self):
        #basic setup 
        self.root = Tk()
        self.root.geometry("1300x1000")

        screen = Canvas(self.root, height = 1300, width = 1000, bg="#fff")
        screen.grid(row = 0, column = 0, sticky = 'n' )

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

        # self.videolabel = Label(self.root, height = 800, width = 1000) ##CHANGE SO THE FULL VIDEO IS SHOWN 
        # self.videolabel.grid(row = 0, column = 0, rowspan = self.vrow, columnspan = self.vcol, sticky = 'n')

        #multiprocessing
        self.gui_nav = multiprocessing.Queue() 
            #Teleop: [1, 0, 0]
            #Autonomous Docking: [2, x, y]
            #Autonomous Transect Line: [3, x, y]
            #End Nav Process: [4, 0, 0]
        self.nav_gui = multiprocessing.Queue() 

        start_nav_b = Button(screen, text = "Begin Nav Process", command = lambda: navGUI.start_nav_process(self.gui_nav, self.nav_gui, self.testing_queue))
        start_nav_b.grid(row = 0, column = self.vcol + 1, sticky = 'n')

        end_nav_b = Button(screen, text = "Terminate Nav Process", command = lambda: navGUI.terminate_nav_process(self.gui_nav))
        end_nav_b.grid(row = 1, column = self.vcol + 1, sticky = 'n')

        #navigation 
        self.mode = "none"

        start_teleop = Button(screen, text = "Teleop", command = lambda: navGUI.start_teleop(self, self.gui_nav))
        start_teleop.grid(row = 2, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking_init = Button(screen, text = "Initialize Auto Docking", command = lambda: autodockinit(self.snapshot()))
        self.autonomous_docking_init.grid(row = 3, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking = Button(screen, text = "Auto Docking Live", command = lambda: navGUI.start_autonomous_docking(self, self.gui_nav))
        self.autonomous_docking.grid(row = 5, column = self.vcol + 1, sticky = 'n')

        self.end_autonomous = Button(screen, text = "end autonomous", command = lambda: navGUI.end_autonomous(self.gui_nav))
        self.end_autonomous.grid(row = 6, column = self.vcol + 1, sticky = 'n')

        #autonomous testing 
        self.testing_queue = multiprocessing.Queue()
            #[Autodocking slider, Auto Transect Line Slider, Vertical Slider, Horizontal Slider, Pivot Slider]

        self.autodocking_val= DoubleVar(screen, value = 5)
        self.autoline_val = DoubleVar(screen, value = 5)

        Label(screen, text = "_________________________________").grid(row = 7, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "Autonomous Docking Slider").grid(row = 8, column = self.vcol + 1, sticky = 'n')
        self.autodocking_slider = Scale(self.root, variable = self.autodocking_val, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        self.autodocking_slider.grid(row = 9, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "_________________________________").grid(row = 10, column = self.vcol + 1, sticky = 'n')

        Label(screen, text = "Autonomous Transect Line Slider").grid(row = 11, column = self.vcol + 1, sticky = 'n')
        self.autoline_slider = Scale(screen, variable = self.autoline_val, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        self.autoline_slider.grid(row = 12, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "_________________________________").grid(row = 13, column = self.vcol + 1, sticky = 'n')

        # self.autodocking_test = Button(self.root, text = "autodocking test", command = navGUI.testing_auto)
        # self.autodocking_test.grid(row = 12, column = self.vcol + 1, sticky = 'n')

        #Nav Mode 
        self.mode_label = Label(screen, text = self.mode)
        self.mode_label.grid(row = 14, column = self.vcol + 1)

        #Nav Sliders 

        self.vmax_val = DoubleVar(screen, value = 75)
        self.lmax_val = DoubleVar(screen, value = 75)
        self.pmax_val = DoubleVar(screen, value = 75)

        Label(screen, text = "_________________________________").grid(row = 715, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "Vertical Max Slider").grid(row = 16, column = self.vcol + 1, sticky = 'n')
        self.vertical_max = Scale(screen, variable = self.vmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.vertical_max.grid(row = 17, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "_________________________________").grid(row = 18, column = self.vcol + 1, sticky = 'n')

        Label(screen, text = "Lateral Max Slider").grid(row = 20, column = self.vcol + 1, sticky = 'n')
        self.lateral_max = Scale(screen, variable = self.lmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.lateral_max.grid(row = 21, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "_________________________________").grid(row = 22, column = self.vcol + 1, sticky = 'n')

        Label(screen, text = "Pivot Max Slider").grid(row = 24, column = self.vcol + 1, sticky = 'n')
        self.pivot_max = Scale(screen, variable = self.pmax_val, from_ = 1, to = 100, orient = HORIZONTAL, length = 200)
        self.pivot_max.grid(row = 25, column = self.vcol + 1, sticky = 'n')
        Label(screen, text = "_________________________________").grid(row = 26, column = self.vcol + 1, sticky = 'n')
        
        #testing cameras 
        self.camera_testing = Button(screen, text = "Assign Cameras", command = self.checkCameras)
        self.camera_testing.grid(row = 27, column = self.vcol + 1, sticky = 'n')
        # #insert Button/Label 

    def showFrames(self):
        self.camerafeedpath = "/Users/valeriefan/Desktop/MATE ROV 2023 /camerafeed.jpg"
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
        self.videolabel.after(20, self.showFrames)

    def snapshot(self):
        cv2.imwrite("/Users/valeriefan/Desktop/MATE ROV 2023 /videosnapshot.png", self.cap2.read()[1])
        return("/Users/valeriefan/Desktop/MATE ROV 2023 /videosnapshot.png") 
    
    def update_mode_label(self):
        self.mode_label.config(text = self.mode)
        self.update_mode_label.after(20, self.update_mode_label)
    
    def send_testing_queue(self):
        #send through queue
        self.coeffs = [self.autodocking_slider.get(), self.autoline_slider.get(), self.vmax_val.get(), self.lmax_val.get(), self.pmax_val.get()]
        # print(self.coeffs)
        self.testing_queue.put(self.coeffs)

        #loop every 20 ms
        self.root.after(20, lambda: self.send_testing_queue())

    def checkCameras(self):
        cv2.imshow("camera 1", self.cap.read()[1])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        camera1 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
        self.assignCamera(self.cap, camera1)
        if cv2.VideoCapture(1).isOpened():
            cv2.imshow("camera 2", self.cap2.read()[1])
            cv2.waitKey(0)
            camera2 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
            self.assignCamera(self.cap2, camera2)
        if cv2.VideoCapture(2).isOpened():
            cv2.imshow("camera 3", self.cap3.read()[1])
            cv2.waitKey(0)
            camera3 = askinteger("1 for front, 2 for claw, 3 for down", "Which camera view is this?")
            self.assignCamera(self.cap3, camera3)

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

    def run(self):
        while True:
            self.root.update()

if __name__ == "__main__":
    gui = GUIClass()
    # gui.showFrames()
    gui.send_testing_queue()
    # gui.checkCameras()
    gui.run()

 