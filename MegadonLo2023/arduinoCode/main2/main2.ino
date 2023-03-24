#include <Servo.h>

int pwmVals[6];

/*
 * [0] lf
 * [1] lb
 * [2] rf
 * [3] rb
 * [4] vl
 * [5] vr
 */

Servo LF_T; //left front
Servo LB_T; //left back
Servo RF_T; //right front
Servo RB_T; //right back
Servo L_VERT; //left vertical
Servo R_VERT; //left vertical
Servo thrusters[] = {LF_T, LB_T, RF_T, RB_T, L_VERT, R_VERT};
// 8, 9, 10, 11, 12, 13

String sendBack;

void setup() {
Serial.begin(9600); // set the baud rate
delay(300);

//Attaching thrusters to PWM pins on arduino
for(int i = 0; i<6; i++){
  thrusters[i].attach(i+8);
  }
}


void loop() {
  
  if(Serial.available()){
    readSerial();
  }
  
  moveThrusters();

  depthPID();  // not made yet

  Serial.println(createSendString());

  delay(50);

}


//reading serial data from python
void readSerial(){
  for(int i = 0; i<5; i++){
    pwmVals[i] = Serial.readStringUntil(',').toInt();
  }
  pwmVals[5] = Serial.readStringUntil('.').toInt();
}


//writing to thrusters
void moveThrusters(){
  for(int i = 0; i<6; i++){
    thrusters[i].writeMicroseconds(pwmVals[i]);
  }
}


//creating string to send back to python
String createSendString(){
  sendback = "";
  for(int i = 0; i<6; i++){
    sendBack += String(pwmVals[i]) + ",";
  }
  return sendBack;
}
