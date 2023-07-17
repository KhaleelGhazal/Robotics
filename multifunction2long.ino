int leftSensor = 0; 
int rightSensor = 0; 
int middleSensor = 0; 
int leftSensorPin = 6;
int rightSensorPin = 10;
int middleSensorPin = 8;
int lower_threshold = 20; 
const int motorLeftForward=2;
const int motorLeftBackward=3;
const int motorRightForward=4;
const int motorRightBackward=7;
const int enablePin = 5;
int value = 0;
float voltage;
float perc;

#include <NewPing.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Servo.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define TRIGGER_PIN 12
#define ECHO_PIN 11
#define MAX_DISTANCE 200

boolean goesForward = false;
int distance = 100;



// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

Servo myServo;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);


void setup() {
  // put your setup code here, to run once:
  pinMode(leftSensorPin, INPUT);
  pinMode(middleSensorPin, INPUT);
  pinMode(rightSensorPin, INPUT);
  pinMode(motorLeftForward, OUTPUT);
  pinMode(motorLeftBackward, OUTPUT);
  pinMode(motorRightForward, OUTPUT);
  pinMode(motorRightBackward, OUTPUT);
  myServo.attach(9);
  Serial.begin(115200);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  myServo.write(115);
  delay(2000);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
  distance = readPing();
  delay(100);
}
void brake(){
  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorRightForward, LOW);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightBackward, LOW);
}
void update_sensors(){ 
// this will read sensor 1 
 leftSensor = digitalRead(leftSensorPin); 
// this will read sensor 2 
 rightSensor = digitalRead(rightSensorPin); 
 // this will read sensor 3
 middleSensor = digitalRead(middleSensorPin); 
}
int lookRight(){  
  myServo.write(50);
  delay(500);
  int distance = readPing();
  delay(100);
  myServo.write(115);
  return distance;
}

int lookLeft(){
  myServo.write(170);
  delay(500);
  int distance = readPing();
  delay(100);
  myServo.write(115);
  return distance;
  delay(100);
}
int readPing(){
  delay(10);
  int proximity = sonar.ping_cm();
  if (proximity==0){
    proximity=250;
  }
  return proximity;
}
void moveForward(){
  if(!goesForward){
    goesForward=true;
    analogWrite(enablePin, 150);
    digitalWrite(motorLeftForward, HIGH);
    digitalWrite(motorRightForward, HIGH);
    digitalWrite(motorLeftBackward, LOW);
    digitalWrite(motorRightBackward, LOW); 
  }
}

void moveBackward(){
  goesForward=false;
  analogWrite(enablePin, 150);
  digitalWrite(motorLeftBackward, HIGH);
  digitalWrite(motorRightBackward, HIGH);
  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorRightForward, LOW);
}

void turnRight(){
  analogWrite(enablePin, 150);
  digitalWrite(motorLeftForward, HIGH);
  digitalWrite(motorRightBackward, HIGH);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightForward, LOW);
  delay(500);
  digitalWrite(motorLeftForward, HIGH);
  digitalWrite(motorRightForward, HIGH);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightBackward, LOW);
}

void turnLeft(){
  analogWrite(enablePin, 150);
  digitalWrite(motorLeftBackward, HIGH);
  digitalWrite(motorRightForward, HIGH);
  digitalWrite(motorLeftForward, LOW);
  digitalWrite(motorRightBackward, LOW);
  delay(500);
  digitalWrite(motorLeftForward, HIGH);
  digitalWrite(motorRightForward, HIGH);
  digitalWrite(motorLeftBackward, LOW);
  digitalWrite(motorRightBackward, LOW);
}

void loop() {
  //digitalWrite(motorLeftForward, HIGH);
  //digitalWrite(motorLeftBackward, HIGH);
  //digitalWrite(motorRightForward, HIGH);
  //digitalWrite(motorRightBackward, HIGH);
  //Serial.println(digitalRead(switchPin));
 
  //Serial.println(proximity);
  value = analogRead(A0);
  voltage = value * 5.0/1023;
  perc = map(voltage, 3.6, 4.2, 0, 100);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 8);
  display.println("STATUS: ARMED");
  display.setCursor(0, 20);
  display.println("BATTERY: ");
  display.setCursor(50, 20);
  display.println(perc);
  display.setCursor(90, 20);
  display.println("%");
  display.setCursor(0, 30);
  display.println("VOLTAGE: ");
  display.setCursor(50, 30);
  display.println(voltage);
  display.setCursor(80, 30);
  display.println("V");

  // Serial.print("Voltage= ");
  // Serial.println(voltage);
  // Serial.print("Battery level= ");
  // Serial.print(perc);
  // Serial.println(" %");
  // delay(500);
  if (digitalRead(A3) == 0){
    display.setCursor(0, 40);
    // Display static text
    display.println("MODE: OBSTACLE AVOIDANCE");
    display.display();
    int distanceRight = 0;
    int distanceLeft = 0;
    delay(10);
    if (distance <= 20){
      brake(); // obstacle probably on the route forward, so stop
      delay(300);
      moveBackward();
      delay(400);
      brake();
      delay(300);
      distanceRight = lookRight();
      delay(300);
      distanceLeft = lookLeft();
      delay(300);
      if (distance >= distanceLeft){
        turnRight(); // calculate in which direction the obstacle is farther
        brake();
      }
      else{
        turnLeft();
        brake();
      }
    }
    else{
    moveForward(); 
    }
    distance = readPing();
 }
 else{
    myServo.write(90); 
    update_sensors();
    display.setCursor(0, 40);
    // Display static text
    display.println("MODE: LINE FOLLOWING");
    display.display();
    //Serial.println(leftSensor);
    //Serial.println(rightSensor);
    //Serial.println(middleSensor);
    if (leftSensor == 0 && rightSensor == 0 && middleSensor == 1){
      analogWrite(enablePin, 130);
      digitalWrite(motorLeftForward, HIGH);
      digitalWrite(motorRightForward, HIGH);
      digitalWrite(motorLeftBackward, LOW);
      digitalWrite(motorRightBackward, LOW); 
    }
    if (leftSensor == 1 && middleSensor == 1 && rightSensor == 0){
      analogWrite(enablePin, 130);
      digitalWrite(motorLeftForward, LOW);
      digitalWrite(motorRightForward, HIGH);
      digitalWrite(motorLeftBackward, HIGH);
      digitalWrite(motorRightBackward, LOW); 
    }
    if (leftSensor == 1 && middleSensor == 0 && rightSensor == 0){
      analogWrite(enablePin, 130);
      digitalWrite(motorLeftForward, LOW);
      digitalWrite(motorRightForward, HIGH);
      digitalWrite(motorLeftBackward, LOW);
      digitalWrite(motorRightBackward, LOW);
    }
    if (leftSensor == 0 && middleSensor == 1 && rightSensor == 1){
      analogWrite(enablePin, 130);
      digitalWrite(motorLeftForward, HIGH);
      digitalWrite(motorRightForward, LOW);
      digitalWrite(motorLeftBackward, LOW);
      digitalWrite(motorRightBackward, HIGH); 
    }
    if (leftSensor == 0 && middleSensor == 0 && rightSensor == 1){
      analogWrite(enablePin, 130);
      digitalWrite(motorLeftForward, HIGH);
      digitalWrite(motorRightForward, LOW);
      digitalWrite(motorLeftBackward, LOW);
      digitalWrite(motorRightBackward, LOW);
    }
    if (leftSensor == 1 && middleSensor == 1 && rightSensor == 1){
      brake();
    }
    if (leftSensor == 0 && middleSensor == 0 && rightSensor == 0){
      brake();
    }
 }
}
