

def PWM(joyVal): #converting a double to a PWM value
    Limit = 400 #with 400 the max is 1900 and the min is 1100 PWM
    joyVal = joyVal*Limit
    return joyVal

#note: modified funciton here to return array of PWM values, instead of a string
def makeCalc(Lx, Ly, Rx, A, B, mode):
    #Lx-Double/float, Ly-Double/float, Rx-Double/float, A-Boolean, B-Boolean, "Sensitive Mode" - Boolean
    v1 = v2 = fr = fl = br = bl = 1500
    sendStr = "" #constructed string to be sent to the arduino
    capMovement = 200
    capPivot = 100
    Vstrength = 200 #vertical thruster code chunks
    expMulti = 1.2
    Ly = Ly * (-1)
    # Lx = Lx * (-1)  #not sure if Lx is inversed, make changes accordingly
    
    
    #deadband 0.1 deviation
    if(Lx < 0.1 and Lx > -0.1):
        Lx = 0
    if(Ly < 0.1 and Ly > -0.1):
        Ly = 0

    #LINEAR MODE
    #if button is not pressed
    if (mode <= 0.5):

        # Front and Back Calculations (cap is 200)
        br += PWM(Ly) * (capMovement/400) 
        bl += PWM(Ly) * (capMovement/400)
        fr += PWM(Ly) * (capMovement/400)
        fl += PWM(Ly) * (capMovement/400)
        

        #Crabbing Calculations (cap is 200)
        br += PWM(Lx)  * (capMovement/400)
        bl += -PWM(Lx) * (capMovement/400)
        fr += -PWM(Lx) * (capMovement/400)
        fl += PWM(Lx)  * (capMovement/400)
        

        #Pivoting CALCULATIONS (cap is 100)
        br += -PWM(Rx) * (capPivot/400)
        bl += PWM(Rx)  * (capPivot/400)
        fr += -PWM(Rx) * (capPivot/400)
        fl += PWM(Rx)  * (capPivot/400)
        

    #EXP MODE
    else:

        # Front and Back Calculations (cap is 200)
        br += (PWM(Ly**expMulti)) * (capMovement/400)
        bl += (PWM(Ly**expMulti)) * (capMovement/400)
        fr += (PWM(Ly**expMulti)) * (capMovement/400)
        fl += (PWM(Ly**expMulti)) * (capMovement/400)
        print(br)
        

        #Crabbing Calculations (cap is 200)
        br += (PWM(Lx**expMulti))  * (capMovement/400)
        bl += -(PWM(Lx**expMulti)) * (capMovement/400)
        fr += -(PWM(Lx**expMulti)) * (capMovement/400)
        fl += (PWM(Lx**expMulti))  * (capMovement/400)
        

        #Pivoting CALCULATIONS (cap is 100)
        br += -(PWM(Rx**expMulti)) * (capPivot/400)
        bl += (PWM(Rx**expMulti))  * (capPivot/400)
        fr += -(PWM(Rx**expMulti)) * (capPivot/400)
        fl += (PWM(Rx**expMulti))  * (capPivot/400)



    #up-down movement
    if(A): #if A is pressed
        v1 += Vstrength
        v2 += Vstrength
        #v1 and v2 go up
    if(B): #if B is pressed
        v1 -= Vstrength
        v2 -= Vstrength
        #v1 and v2 go down

    #capping the pwm values at 1900/1100, also rounding them to the whole number
    pwmArray = [fr, fl, br, bl, v1, v2]
    for index in range(len(pwmArray)):

        
        #cap
        pwmArray[index] = max(1100, pwmArray[index])
        pwmArray[index] = min(1900, pwmArray[index])
    

    # sends the PWM values in the order:
    # fr, fl, br, bl, v1, v2
    return pwmArray


    






 