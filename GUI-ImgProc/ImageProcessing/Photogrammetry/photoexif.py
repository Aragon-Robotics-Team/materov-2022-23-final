import cv2
import time
import keyboard
import tkinter as tk

from exif import Image
import globalvars 

#Press the button to start the program
#Press s to take as many photos as you want

def takePhotos():
    videoCaptureObject = cv2.VideoCapture(0)

    i = 0
    while True:
        ret, frame = videoCaptureObject.read()
        cv2.imshow("Capturing Video", frame)
            # deletes every frame as the next one comes on, closes all windows when q i`s pressed
        if cv2.waitKey(1) == ord('q'):
            videoCaptureObject.release()
            cv2.destroyAllWindows()
            break
                # when s is pressed
        # folder_path = "/Users/valeriefan/Desktop/materovip/test2"
        folder_path = globalvars.folder_path
        if cv2.waitKey(1) == ord('s'):
            # and the index is less than txhe length of the snapshot list
            # take as snapshot, save it, show it
            #/Users/valeriefan/Desktop/materovip/{i}.png  
            cv2.imwrite(f"{folder_path}/{i}.JPG", frame)
            cv2.imshow(f"{folder_path}/{i}.JPG", frame)
            addExif(folder_path, f"{i}.JPG")

            # cv2.imwrite(f"C://Users//alexa//Desktop//potos//picture//{i}.png", frame)
            # cv2.imshow(f"C://Users//alexa//Desktop//potos//picture//{i}.png", frame)
            cv2.waitKey(0)
            i += 1
        else:
            result = False
    
def addExif(folder, img_name):
    # print(img_path)
    folder_path = folder
    with open(f"{folder_path}/{img_name}", 'rb') as img_file:
        img = Image(img_file)
    print(img.has_exif)
    # sorted(img.list_all())
    
    # img.focal_length = 3.6
    # img.make = "opencv screenshot"
    # img.model = "zosi cctv"
    img.focal_length = 23
    img.make = "IPhone"
    img.model = "13"
    # print(f'Focal Length: {img.get("focal_length")}')
    print("set focal length, make, and model")

    with open(f'{folder_path}/modified/{img_name}', 'wb') as new_image_file:
        new_image_file.write(img.get_file())
    print("saved")

def existingFolder(folder_path):
    i=4
    while i < 42:
        addExif(folder_path, f"{i}.JPG")
        print(f"exif added to {i}")
        i+=1

def takeVideo(cap):
    videoCaptureObject = cap
    i = 0
    while True:
        ret, frame = videoCaptureObject.read()
        cv2.imshow("Capturing Video", frame)
            # deletes every frame as the next one comes on, closes all windows when q i`s pressed
        # folder_path = "/Users/valeriefan/Desktop/materovip/test2"
        folder_path = globalvars.folder_path
        cv2.imwrite(f"{folder_path}/{i}.JPG", frame)
        cv2.imshow(f"{folder_path}/{i}.JPG", frame)
        cv2.destroyAllWindows()
        addExif(folder_path, f"{i}.JPG")
        i += 1
        if cv2.waitKey(1) == ord('q'):
            videoCaptureObject.release()
            cv2.destroyAllWindows()
            break

        # cv2.imwrite(f"C://Users//alexa//Desktop//potos//picture//{i}.png", frame)
        # cv2.imshow(f"C://Users//alexa//Desktop//potos//picture//{i}.png", frame)


# root = tk.Tk()
# run = tk.Button(text="Start Photo Taking", command=takePhotos).pack()

# root.mainloop()

# if __name__ == "__main__":
    # existingFolder("/Users/valeriefan/Desktop/materovip/bowltest")
    # existingFolder("/Users/valeriefan/Desktop/materovip/test5")
    # addExif("/Users/valeriefan/Desktop/materovip/0.JPG")
    # addExif("/Users/valeriefan/Desktop/IMG_8064.JPG")
    # addExif("/Users/valeriefan/Desktop/test.JPG")
    # addExif("/Users/valeriefan/Desktop/18.jpeg")
    # addExif("/Users/valeriefan/Desktop/materovip/test2/0.JPG")
    # addExif("0.JPG")



