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

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.title('Megalodon ROV GUI 0.1.0')
window.geometry(f'{screen_width}x{screen_height}')

print(screen_width)
print(screen_height)

screenheight = int(0.5*screen_height)
screenwidth = int(0.25*screen_width)

class GUIClass():
    def __init__(self):
        #basic setup 

        screen = Canvas(window, height = screenheight, width = 1000, bg="#fff")
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
        self.autodocking_slider = Scale(window, variable = self.autodocking_val, from_ = 1, to = 1000, orient = HORIZONTAL, length = 200)
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
        window.after(20, lambda: self.send_testing_queue())

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
            window.update()

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

# window = tk.Tk()
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
# window.title('Megalodon ROV GUI 0.1.0')
# window.geometry(f'{screen_width}x{screen_height}')

print(screen_width)
print(screen_height)

def web():
    webbrowser.open("http://www.aragonrobotics.org/")

screenheight = int(0.5*screen_height)
screenwidth = int(0.25*screen_width)

# screen = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
# screen.grid(row = 0, column = 0, sticky = 'n' )

# screen1 = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
# screen1.grid(row = 1, column = 0, sticky = 'n' )

# placer = Canvas(window, height = 0.5*screen_height, width = 2*screenwidth, bg="#f4f4f4")
# placer.grid(row = 0, column = 1, sticky = 'n' )

# screen2 = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
# screen2.grid(row = 0, column = 2, sticky = 'n' )

# button1 = tk.Button(text="GUI",width=50,height=2,fg="black", command=web).place(x=0.1*screen_width, y=0.1*screen_height)
# button2 = tk.Button(text="GUI",width=10,heiqght=1,fg="black", command=web).place(x=0, y=0)

#
# Button(screen, text='Button2', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.01*screenheight)
# Button(screen, text='Button3', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.125*screenheight)
# Button(screen, text='Button4', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.234*screenheight)
# Button(screen, text='Button5', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.340*screenheight)
# Button(screen, text='Button6', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.445*screenheight)
#

# adding scrollbar
# scrollbar = Scrollbar(screen2)
  
# packing scrollbar
# scrollbar.pack(side=RIGHT,fill=Y)
  
# text_info = Text(screen2,yscrollcommand=scrollbar.set)
# text_info.pack(fill=BOTH)
  
# configuring the scrollbar
# scrollbar.config(command=text_info.yview)

#EMERGENCY HALT ------------------------------------------------------------------------------------------------------------

def enableBot():
    global autoArray
    autoArray[1] = 0
    output_queue.put(autoArray)
    print ("BOT ENABLED")

def disableBot():
    global autoArray
    autoArray[1] = 1
    output_queue.put(autoArray)
    print("BOT DISABLED")

# startBot = Button( text = "Enable Bot", command = enableBot, width = 50, height = 2, fg = 'green', bg = 'gray').place(x=.2*screen_width, y= .8*screen_height)

# stopBot = Button( text = "Disable Bot (Emergency Halt)", command = disableBot, width = 50, height = 2, fg = 'red', bg = "gray").place(x=.55*screen_width,y = .8*screen_height)

# # # # # # # # # # # # # # # # # 

cap = cv2.VideoCapture(0)

#SETUP ------------------------------------------------------------------------------------------------------

style =  ttk.Style()

style.theme_create( "button-center", parent="alt", settings={"TButton": {"configure": {"anchor": "center"}}} )

style.configure('TButton', font = ('Helvetica', 13), width = 25)

vcol = 3
#VIDEO FEED ------------------------------------------------------------------------------------------------------
e = int(screen_width*0.5)

label = Label(window, height = 500, width = e) ##CHANGE SO THE FULL VIDEO IS SHOWN 

label.place(x=0.255*screen_width,y=0.05*screen_height)

# from threading import Thread
# import cv2, time

# class ThreadedCamera(object):
#     def __init__(self, src=0):
#         self.capture = cv2.VideoCapture(src)
#         self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
       
#         # FPS = 1/X
#         # X = desired FPS
#         self.FPS = 1/30
#         self.FPS_MS = int(self.FPS * 1000)
        
#         # Start frame retrieval thread
#         self.thread = Thread(target=self.update, args=())
#         self.thread.daemon = True
#         self.thread.start()
        
#     def update(self):
#         while True:
#             if self.capture.isOpened():
#                 (self.status, self.frame) = self.capture.read()
#             time.sleep(self.FPS)
            
#     def show_frame(self):
#         cv2.imshow('frame', self.frame)
#         cv2.waitKey(self.FPS_MS)

# if __name__ == '__main__':
#     src = 'https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w1421640637.m3u8'
#     threaded_camera = ThreadedCamera(src)
#     while True:
#         try:
#             threaded_camera.show_frame()
#         except AttributeError:
#             pass

# def showFrames():
#     cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
#     img = Image.fromarray(cv2image)
#     # Convert image to PhotoImage
#     imgtk = ImageTk.PhotoImage(image = img)
#     label.imgtk = imgtk
#     label.configure(image=imgtk)
#     # Repeat after an interval to capture continiously
#     label.after(20, showFrames)

# showFrames()
#USB INPUT ------------------------------------------------------------------------------------------------------
usb = tk.Label(text="USB Input:").place(x=1138,y=5)

import os

os.system("color")

Usb = os.popen("wmic logicaldisk where drivetype=2 get description ,deviceid ,volumename").read()
print(Usb)

def check(DeviceID):
    if Usb.find(str(DeviceID)) != -1:
        print("\033[1;32mUsb is plugged")
        yes = tk.Label(text="Connected",fg="green").place(x=1195,y=5)
        input("")

    else:
        print("\033[0;31mUsb is not plugged")
        no = tk.Label(text="Disconnected",fg="red").place(x=1195,y=5)
        input("")

i = "1"
while i < "2":
    check(1)
    #check(-"DEVICE ID HERE"-)

##

if __name__ == "__main__":
    gui = GUIClass()
    # gui.showFrames()
    gui.send_testing_queue()
    # gui.checkCameras()
    gui.run()
    window.mainloop()