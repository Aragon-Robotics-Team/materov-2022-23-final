#include <Servo.h>

//global variables for thruster pwms
int RB_PWM;
int LF_PWM;
int LB_PWM;
int RF_PWM;
int v1;
int v2;

Servo LF_T; //left front
Servo LB_T; //left back
Servo RF_T; //right front
Servo RB_T; //right back
Servo F_VERT; //left vertical
Servo B_VERT; //left vertical


void setup() {
  Serial.begin(9600); // set the baud rate
  Serial.println("Arduino is ready!");

////Attaching thrusters to PWM pins on arduino
//  LF_T.attach(8); 
//  LB_T.attach(9);
//  RF_T.attach(10);
//  RB_T.attach(11);
//  L_VERT.attach(12); //check 6 and 7 pins(if they are pwm)
//  R_VERT.attach(13);
  LF_T.attach(13); 
  RB_T.attach(12);
  LB_T.attach(11);
  RF_T.attach(10);
  F_VERT.attach(9); //check 6 and 7 pins(if they are pwm)
  B_VERT.attach(8);
  
}



void loop() {

  if (Serial.available()) {
   
    //getting PWM values pyserial
    RF_PWM = Serial.readStringUntil('-').toInt();
    LF_PWM = Serial.readStringUntil('=').toInt();
    RB_PWM = ((Serial.readStringUntil('+').toInt() - 1500) * (-1)) + 1500;
    LB_PWM = Serial.readStringUntil('*').toInt();
    v1 = Serial.readStringUntil(',').toInt();
    v2 = Serial.readStringUntil('.').toInt();
  
    //send pwm values to thrusters
    LF_T.writeMicroseconds(LF_PWM);
    LB_T.writeMicroseconds(LB_PWM);
    RF_T.writeMicroseconds(RF_PWM);
    RB_T.writeMicroseconds(RB_PWM);
    F_VERT.writeMicroseconds(v1);
    B_VERT.writeMicroseconds(v2);
    
    //note: RB is adjusted to its actual "value" when printed by serial
    Serial.println("RB_PWM: " + String((RB_PWM - 1500) * (-1) + 1500) + ", " +
                   "LF_PWM: " + String(LF_PWM) + ", " + 
                   "LB_PWM: " + String(LB_PWM) + ", " + 
                   "RF_PWM: " + String(RF_PWM) + ", " + 
                   "V1: " + String(v1) + ", " + 
                   "V2: " + String(v2));
    
    delay(50);
  }
}