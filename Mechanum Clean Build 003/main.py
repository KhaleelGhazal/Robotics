from machine import Pin, I2C, UART, PWM
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import math
import time
from time import sleep


WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl = Pin(17), sda = Pin(16), freq = 200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)


servo = PWM(Pin(27))
servo.freq(50)

debounce_time=0
button = Pin(10, Pin.IN, Pin.PULL_UP)
mode = 0

frontRightForward = PWM(Pin(3))
frontRightForward.freq(50)
frontRightBackward = PWM(Pin(2))
frontRightBackward.freq(50)
backRightBackward = PWM(Pin(4))
backRightBackward.freq(50)
backRightForward = PWM(Pin(5))
backRightForward.freq(50)
backLeftForward = PWM(Pin(6))
backLeftForward.freq(50)
backLeftBackward = PWM(Pin(7))
backLeftBackward.freq(50)
frontLeftForward = PWM(Pin(8))
frontLeftForward.freq(50)
frontLeftBackward = PWM(Pin(9))
frontLeftBackward.freq(50)



trigger = Pin(19, Pin.OUT)
echo = Pin(18, Pin.IN)

IRL = Pin(20, Pin.IN)
IRR = Pin(21, Pin.IN)
leftSensor = Pin(15, Pin.IN)
middleSensor = Pin(14, Pin.IN)
rightSensor = Pin(13, Pin.IN)
leftValue = -1
rightValue = -1
middleValue = -1
leftFrontValue = -1
rightFrontValue = -1


Up = 24
Down = 82
Left = 8
Right = 90
Brake = 28



uart = UART(0, 9600)
dt = "N"

def forward():
    frontRightForward.duty_u16(20000)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(20000)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(20000)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(20000)
    backLeftBackward.duty_u16(0)
    
def backward():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(20000)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(20000)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(20000)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(20000)

def left():
    frontRightForward.duty_u16(20000)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(20000)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(20000)
    backLeftForward.duty_u16(20000)
    backLeftBackward.duty_u16(0)
    
def right():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(20000)
    frontLeftForward.duty_u16(20000)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(20000)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(20000)

def diag45():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(20000)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(20000)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(0)
    
def diag225():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(20000)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(20000)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(0)
    
def pivotRightForward():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(20000)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(20000)
    backLeftBackward.duty_u16(0)
    
def pivotRightBackward():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(20000)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(20000)
    
def pivotLeftForward():
    frontRightForward.duty_u16(20000)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(20000)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(0)
    
def pivotLeftBackward():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(20000)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(20000)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(0)
    
def rotCW():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(20000)
    frontLeftForward.duty_u16(20000)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(20000)
    backLeftForward.duty_u16(20000)
    backLeftBackward.duty_u16(0)
    
def rotCCW():
    frontRightForward.duty_u16(20000)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(20000)
    backRightForward.duty_u16(20000)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(20000)
    
def brake():
    frontRightForward.duty_u16(0)
    frontRightBackward.duty_u16(0)
    frontLeftForward.duty_u16(0)
    frontLeftBackward.duty_u16(0)
    backRightForward.duty_u16(0)
    backRightBackward.duty_u16(0)
    backLeftForward.duty_u16(0)
    backLeftBackward.duty_u16(0)

                

def get_distance():
    trigger.low()
    utime.sleep_us(4)
    trigger.high()
    utime.sleep_us(10)
    trigger.low()
    
    while echo.value() == 0:
        signaloff = utime.ticks_us()
        
    while echo.value() == 1:
        signalon = utime.ticks_us()
        
    timepassed = signalon-signaloff
    distance = (timepassed *0.034) / 2
    
    return distance
def servoLeft():
    servo.duty_u16(7800) #1500-8500
    
def servoRight():
    servo.duty_u16(3000) #1500-8500
    
def servoStart():
    servo.duty_u16(5400) #1500-8500
 
def updateBottomSensors():
    global leftValue
    global middleValue
    global rightValue
    leftValue = leftSensor.value()
    middleValue = middleSensor.value()
    rightValue = rightSensor.value()
    
def updateFrontSensors():
    global leftFrontValue
    global rightFrontValue
    leftFrontValue = IRL.value()
    rightFrontValue = IRR.value()
        
servoStart()
distance = get_distance()

while True:
    oled.fill(0)
    oled.text("STATUS: ARMED", 0, 30)
    oled.text("MODE:", 0, 45)
    if uart.any() > 0:
        dt = uart.read()
        print(dt)
    if ((button.value() is 0) and (time.ticks_ms()-debounce_time) > 300):
        mode+=1
        if mode == 4:
            mode = 0
        debounce_time=time.ticks_ms() 
    if mode == 0:
        oled.text("COLL. AV", 40, 45)
        oled.show()
        distance = get_distance()
        if distance < 20:
            brake()
            time.sleep(0.5)
            servoLeft()
            time.sleep(0.3)
            leftDis = get_distance()
            time.sleep(0.3)
            servoStart()
            time.sleep(0.3)
            servoRight()
            time.sleep(0.3)
            rightDis = get_distance()
            time.sleep(0.3)
            servoStart()
            if(leftDis > rightDis):
                left()            
                time.sleep(0.5)
                brake()
                time.sleep(0.5)
            elif(leftDis < rightDis):
                right()
                time.sleep(0.5)
                brake()
                time.sleep(0.5)
        else:
            leftDis = 0
            rightDis = 0
            forward()
    if mode == 1:
        oled.text("LINE F.", 40, 45)
        oled.show()
        updateBottomSensors()
        if leftValue == 0 and rightValue == 0 and middleValue == 1:
            forward()
        if leftValue == 1 and rightValue == 0 and middleValue == 1:
            left()
        if leftValue == 1 and rightValue == 0 and middleValue == 0:
            left()
        if leftValue == 0 and rightValue == 1 and middleValue == 1:
            right()
        if leftValue == 0 and rightValue == 1 and middleValue == 0:
            right()
        if leftValue == 0 and rightValue == 0 and middleValue == 0:
            brake()
        if leftValue == 1 and rightValue == 1 and middleValue == 1:
            brake()
            
    if mode == 2:
        oled.text("HAND F.", 40, 45)
        oled.show()
        updateFrontSensors()
        distance = get_distance()
        if distance > 10 and distance < 18:
            forward()
        elif distance < 10:
            brake()
        elif rightFrontValue == 0 and leftFrontValue == 1:
            right()
        elif rightFrontValue == 1 and leftFrontValue == 0:
            left()
        elif distance > 18:
            brake()
            
    if mode == 3:
        oled.text("MOBILE", 40, 45)
        oled.show()
        if dt == b'1':
            forward()
        elif dt == b'2':
            backward()
        elif dt == b'3':
            right()
        elif dt == b'Z':
            pivotLeftForward()
        elif dt == b'Y':
            brake()
        elif dt == b'X':
            pivotRightForward()
        elif dt == b'W':
            brake()
        elif dt == b'V':
            pivotLeftBackward()
        elif dt == b'U':
            brake()
        elif dt == b'T':
            pivotRightBackward()
        elif dt == b'S':
            brake()
        elif dt == b'Q':
            rotCW()
        elif dt == b'K':
            brake()
        elif dt == b'4':
            left()
        elif dt == b'5':
            brake()
        elif dt == b'6':
            brake()
        elif dt == b'7':
            brake()
        elif dt == b'8':
            brake()
        elif dt == b'C':
            brake()
            mode = 0
        elif dt == b'L':
            brake()
            mode = 1
        elif dt == b'H':
            brake()
            mode = 2
        elif dt == b'R':
            brake()
            mode = 3
        
    
        
