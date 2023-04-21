from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
import cv2 
import multiprocessing 

from PIL import Image, ImageTk 

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.title('Megalodon ROV GUI 0.1.0')
window.geometry(f'{screen_width}x{screen_height}')

print(screen_width)
print(screen_height)

def web():
    webbrowser.open("http://www.aragonrobotics.org/")

screenheight = int(0.5*screen_height)
screenwidth = int(0.25*screen_width)

screen = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
screen.grid(row = 0, column = 0, sticky = 'n' )

screen1 = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
screen1.grid(row = 1, column = 0, sticky = 'n' )

placer = Canvas(window, height = 0.5*screen_height, width = 2*screenwidth, bg="#f4f4f4")
placer.grid(row = 0, column = 1, sticky = 'n' )

screen2 = Canvas(window, height = screenheight, width = screenwidth, bg="#fff")
screen2.grid(row = 0, column = 2, sticky = 'n' )

# button1 = tk.Button(text="GUI",width=50,height=2,fg="black", command=web).place(x=0.1*screen_width, y=0.1*screen_height)
# button2 = tk.Button(text="GUI",width=10,heiqght=1,fg="black", command=web).place(x=0, y=0)

#
Button(screen, text='Button2', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.01*screenheight)
Button(screen, text='Button3', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.125*screenheight)
Button(screen, text='Button4', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.234*screenheight)
Button(screen, text='Button5', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.340*screenheight)
Button(screen, text='Button6', command=web, width = 45, height = 2).place(x=0*screenwidth, y=0.445*screenheight)
#

# adding scrollbar
scrollbar = Scrollbar(screen2)
  
# packing scrollbar
scrollbar.pack(side=RIGHT,fill=Y)
  
text_info = Text(screen2,yscrollcommand=scrollbar.set)
text_info.pack(fill=BOTH)
  
# configuring the scrollbar
scrollbar.config(command=text_info.yview)

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

startBot = Button( text = "Enable Bot", command = enableBot, width = 50, height = 2, fg = 'green', bg = 'gray').place(x=.2*screen_width, y= .8*screen_height)

stopBot = Button( text = "Disable Bot (Emergency Halt)", command = disableBot, width = 50, height = 2, fg = 'red', bg = "gray").place(x=.55*screen_width,y = .8*screen_height)

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

from threading import Thread
import cv2, time

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
#     # src = 'https://videos3.earthcam.com/fecnetwork/9974.flv/chunklist_w1421640637.m3u8'
#     threaded_camera = ThreadedCamera(0)
#     while True:
#         try:
#             threaded_camera.show_frame()
#         except AttributeError:
#             pass

def showFrames():
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    label.after(20, showFrames)

showFrames()
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
    window.mainloop()