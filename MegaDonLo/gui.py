#---------------------------------------
#basic gui imports
from tkinter import *
from tkinter import ttk

#video feed
import cv2
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

        #styling
        self.style =  ttk.Style()
        self.style.theme_create( "button-center", parent="alt", settings={"TButton": {"configure": {"anchor": "center"}}} )
        self.style.configure('TButton', font = ('Helvetica', 13), width = 25)
        self.vcol = 1 #number of columns that the video feed, or else the video is weirdly squished for some reason 
        self.vrow = 1 #number of rows that the video feed needs to span, same reasoning as above 

        #video feed 
        self.cap = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(1)

        # self.videolabel = Label(self.root, height = 800, width = 1000) ##CHANGE SO THE FULL VIDEO IS SHOWN 
        # self.videolabel.grid(row = 0, column = 0, rowspan = self.vrow, columnspan = self.vcol, sticky = 'n')

        #multiprocessing
        self.gui_nav = multiprocessing.Queue() 
            #Teleop: [1, 0, 0]
            #Autonomous Docking: [2, x, y]
            #Autonomous Transect Line: [3, x, y]
            #End Nav Process: [4, 0, 0]
        self.nav_gui = multiprocessing.Queue() 

        start_nav_b = Button(self.root, text = "Begin Nav Process", command = lambda: navGUI.start_nav_process(self.gui_nav, self.nav_gui, self.testing_queue))
        start_nav_b.grid(row = 0, column = self.vcol + 1, sticky = 'n')

        end_nav_b = Button(self.root, text = "Terminate Nav Process", command = lambda: navGUI.terminate_nav_process(self.gui_nav))
        end_nav_b.grid(row = 1, column = self.vcol + 1, sticky = 'n')

        #navigation 
        self.mode = "none"

        start_teleop = Button(self.root, text = "Teleop", command = lambda: navGUI.start_teleop(self, self.gui_nav))
        start_teleop.grid(row = 2, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking_init = Button(self.root, text = "Initialize Auto Docking", command = lambda: autodockinit(self.snapshot()))
        self.autonomous_docking_init.grid(row = 3, column = self.vcol + 1, sticky = 'n')

        self.autonomous_docking = Button(self.root, text = "Auto Docking Live", command = lambda: navGUI.start_autonomous_docking(self, self.gui_nav))
        self.autonomous_docking.grid(row = 5, column = self.vcol + 1, sticky = 'n')

        self.end_autonomous = Button(self.root, text = "end autonomous", command = lambda: navGUI.end_autonomous(self.gui_nav))
        self.end_autonomous.grid(row = 6, column = self.vcol + 1, sticky = 'n')


        #autonomous testing 
        self.testing_queue = multiprocessing.Queue()
            #[Autodocking slider, Auto Transect Line Slider]

        self.autodocking_slider= DoubleVar(self.root, value = 5)
        self.autoline_slider = DoubleVar(self.root, value = 5)

        Label(self.root, text = "_________________________________").grid(row = 7, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "Autonomous Docking Slider").grid(row = 8, column = self.vcol + 1, sticky = 'n')
        BRight = Scale(self.root, variable = self.autodocking_slider, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        BRight.grid(row = 9, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 10, column = self.vcol + 1, sticky = 'n')

        Label(self.root, text = "Autonomous Transect Line Slider").grid(row = 11, column = self.vcol + 1, sticky = 'n')
        BLeft = Scale(self.root, variable = self.autoline_slider, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
        BLeft.grid(row = 12, column = self.vcol + 1, sticky = 'n')
        Label(self.root, text = "_________________________________").grid(row = 13, column = self.vcol + 1, sticky = 'n')

        # self.autodocking_test = Button(self.root, text = "autodocking test", command = navGUI.testing_auto)
        # self.autodocking_test.grid(row = 12, column = self.vcol + 1, sticky = 'n')

        #Nav Mode 
        self.mode_label = Label(self.root, text = self.mode)
        self.mode_label.grid(row = 14, column = self.vcol + 1)
        

        #insert Button/Label 

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
        self.coeffs = [self.autodocking_slider.get(), self.autoline_slider.get()]
        # print(self.coeffs)
        self.testing_queue.put(self.coeffs)

        #loop every 20 ms
        self.root.after(20, lambda: self.send_testing_queue())

    def run(self):
        while True:
            self.root.update()

if __name__ == "__main__":
    gui = GUIClass()
    # gui.showFrames()
    gui.send_testing_queue()
    gui.run()

