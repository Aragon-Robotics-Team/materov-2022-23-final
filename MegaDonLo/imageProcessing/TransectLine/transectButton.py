import cv2
import tkinter as tk
import tkinter as tk

from .TransectLine import findAngle
from .TransectLine import straightLFPWMOutput
from .TransectLine import colorSelector

def startTransect(videoCaptureObject, nav_queue):
    # videoCaptureObject = cv2.VideoCapture(0)
    ret,frame = videoCaptureObject.read()
    B,G,R = colorSelector(frame)
    result = True
    while result:
        ret,frame = videoCaptureObject.read()
        # cv2.imshow("Capturing Video",frame)
        x,y = findAngle(frame, B, G, R)
        nav_queue.put([3, x, y])
        cv2.imshow("linesDetected", frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            videoCaptureObject.release()
            result = False
            cv2.destroyAllWindows()

#root = tk.Tk()
#run = tk.Button(text = "Transect Line", command = startTransect).pack()

#root.mainloop()
