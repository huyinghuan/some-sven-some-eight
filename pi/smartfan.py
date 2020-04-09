import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, GPIO.HIGH)
is_close = True

TEMP = 50

try:
    while True:
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp = int(f.read()) / 1000
            print(temp)
            # turn on
            if temp > TEMP and is_close == True:
                GPIO.output(7, GPIO.LOW)
                is_close = False
                time.sleep(10)
            elif temp <= TEMP and is_close == False:
                GPIO.output(7, GPIO.HIGH)
                is_close = True
                time.sleep(1)
            else:
                time.sleep(1)
except:
     GPIO.output(7, GPIO.HIGH)
