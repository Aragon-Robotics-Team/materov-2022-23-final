#include <Servo.h>

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

int pwmVals[6];
int out_len = 6;  //# of values we want to output
int in_len = 6;  //# of values we are receiving

String serialOutput;
String serialInput;



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

  serialInput = Serial.readStringUntil('.');

  int startIndex = 0;
  int endIndex = 0;

  for(int i = 0; i<6; i++){
    endIndex = serialInput.indexOf(',', startIndex);
    pwmVals[i] = serialInput.substring(startIndex, endIndex);
    startIndex = endIndex + 1;
  }

}


//writing to thrusters
void moveThrusters(){
  for(int i = 0; i<6; i++){
    thrusters[i].writeMicroseconds(pwmVals[i]);
  }
}


//creating string to send back to python
String createSendString(){
  serialOutput = "";
  for(int i = 0; i<out_len; i++){
    serialOutput += String(pwmVals[i]) + ",";
  }
  return serialOutput;
}
