void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available());
  String x = Serial.readStringUntil(',');
  if ( x >= "Arduino" ) {
    Serial.println("Serial Communication established.");
  }

  else{
    //read thruster values and write back
  }

}
