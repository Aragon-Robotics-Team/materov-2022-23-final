
"""
Robot contains the Arduino object, the Gamepad object, and other robot configurations.
Communicates with other processes, namely GUI, and allows Python to communicate with the onboard Arduino.
"""
import pygame
from time import sleep
import serial
from multiprocessing import Queue



class Robot:

    def __init__(self, queue_in: Queue, queue_out: Queue, testing_queue: Queue) -> None:  # gui creates object bot and interacts with it
        # self.gamepad = pygame.joystick.Joystick(0)
        # self.gamepad.init()
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.testing_queue = testing_queue
        self.portNum = 14301
        self.baudRate = 9600
        self.delay = 0.1
        self.arduino = serial.Serial(port=f'/dev/cu.usbmodem{self.portNum}',
                                     baudrate=self.baudRate,
                                     timeout=1)
        sleep(1)

    def get_send_arduino(self, ls: list):
        sendStr = (str(ls[0]) + "-" +
                   str(ls[1]) + "=" +
                   str(ls[2]) + "+" +
                   str(ls[3]) + "*" +
                   str(ls[4]) + "," +
                   str(ls[5]) + ".")
        # print("sending:", sendStr)
        self.arduino.write(sendStr.encode("ascii"))  # write (output) to arduino
        while self.arduino.in_waiting == 0:
            pass
        # print(self.arduino.in_waiting)

        received_data_list = self.arduino.readline().decode("ascii").split(',')  # read input from arduino
        # print("recieving:", received_data_list, '\n\n')
        # self.put_queue(received_data_list)

    def get_queue(self):
        obj = []
        while self.queue_in.empty() == False:
            obj = self.queue_in.get()

        # print('gotten from queue: ')

        return obj

    '''
    list received from queue: 
    [period (0/1/2/-1), target depth]
    '''

    def put_queue(self, obj: list):
        self.queue_out.put(obj)

    #queue specifically for variables that are solely for testing (e.g. slider for autonomous)
    def get_testing_queue(self):
        obj = []
        while self.testing_queue.empty() == False:
            obj = self.testing_queue.get()

        return obj 


if __name__ == '__main__':
    pass

