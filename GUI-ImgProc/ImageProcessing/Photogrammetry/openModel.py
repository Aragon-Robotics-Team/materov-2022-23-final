import os
import ctypes
import argparse

import subprocess
import sys




# parser = argparse.ArgumentParser()

# parser.add_argument('file', help = "file path pls :pleading_face:")

# args = parser.parse_args()
# filePath = args.file

# os.startfile(filePath)

# mymessage = 'Diseased Tissue Total Area: 56in^2\nDiameter: 26in\nHeight: 12in'
# title = 'Print 3D - bowltest2'
# ctypes.windll.user32.MessageBoxW(0, mymessage, title, 0)
#cv2.imshow("camera 1", self.cap.read()[1])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # camera1 = askinteger("1 for front, 2 for claw, 3 for down, 4 for facetime, 5 for other", "Which camera view is this?")
    # assignCamera(self, s
def openModel(filePath, diameter, height):
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, filePath])

    mymessage = f'Diseased Tissue Total Area: 56cm^2\nDiameter: {diameter}cm\nHeight: {height}cm'
    title = 'Print 3D - bowltest2'
    os.system("osascript -e 'Tell application \"System Events\" to display dialog \""+mymessage+"\"'")

if __name__ == "__main__":
    openModel("/Users/valeriefan/Downloads/Magnificent Blad/tinker.obj", 10, 10)
