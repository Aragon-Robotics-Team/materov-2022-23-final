from multiprocessing import Queue
from nav.Robot.Robot import Robot
from ..Teleop.MathFunc import PWM, makeString
from time import sleep

class Autonomous():
    def __init__(self, rob: Robot):

        self.rob = rob

    def begin_and_loop(self):  # Main Loop of Autonomous

        print('AUTONAVSIDE STARTED')

        sleep(10)
        print ("asdf")
        while True:
            qList = self.rob.get_queue()
            if len(qList) != 0:
                # print("Auto queue yes")
                print(qList)
                whichAuto = qList[0]
                x = round(qList[1], 2)  # round vector component to 2 decimal places
                y = round(qList[2], 2)

                if whichAuto == 0:  # exit autonomous
                    break
                if whichAuto == 1:
                    sendStr = self.transectLine(x, y)
                elif whichAuto == 2:
                    sendStr = self.autoDocking(x, y)
                    print("autodocking")

                self.rob.get_send_arduino(sendStr)  # send to Robot arduino comm function
            # self.rob.get_send_arduino([1600, 1600, 1600, 1600, 1600, 1600])  # send to Robot arduino comm function

            print("sent string")
            # sleep(self.rob.delay)


    '''
    Transect Line:
    inputs: 
        x = x-component of screen vector (float)
        y = y-component of screen vector (float)
    output: 
        list of size 6: [fr, fl, br, bl, v1, v2]
    '''
    def transectLine(self, x: float, y: float) -> list:
        #def makeString(Lx, Ly, Rx, A, B, percent_horiz, percent_vert) 
        slider = 1
        Lx=x*slider
        Ly=y*slider
        Rx=0
        A=False
        B=False
        percent_horiz=50
        percent_vert=50

      
        
        return(makeString(Lx, Ly, Rx, A, B, percent_horiz, percent_vert))



    '''
        Auto Docking:
        inputs: 
            x = x-component of screen vector (float)
            y = y-component of screen vector (float)
        output: 
            list of size 6: [fr, fl, br, bl, v1, v2]
        '''
    def autoDocking(self, x: float, y: float) -> list:
        #def makeString(Lx, Ly, Rx, A, B, percent_horiz, percent_vert) 
        slider = 1
        Lx=1
        if(x>0):
            Lx=slider #left and right
        if(x<0):
            Lx=-slider
        Ly=0.2 #going forward
        Rx=0 #no turning
        A=False
        B=False
        if(y>0):
            A=True
        if(y<0):
            B=True
        percent_horiz=100
        percent_vert=100
        
        print("in nav autodocking")
        return makeString(Lx, Ly, Rx, A, B, percent_horiz, percent_vert) 
        
    
