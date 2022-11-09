import waveFunctions as b
import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
values = []
n = 8
levels = 2 ** n
comp = 4
troyka = 17

def decimal2binary(value):
    return [int(elem) for elem in bin(value)[2:].zfill(8)]

def adc():
    result = 0
    weight = levels // 2
    for i in range(n):
        GPIO.output(dac, decimal2binary(result + weight))
        time.sleep(0.005)
        if (GPIO.input(comp) == 1):
            result += weight
        weight //= 2
    return result


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
    b.waitForOpen()
    GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(comp, GPIO.IN)
    GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
    start = time.time()
    current = time.time()
    while current - start < 15:
        adc_value = adc()
        current = time.time()
        values.append(adc_value)
        print("Значение на АЦП: {}".format(adc_value))
    b.save(values, start, current)
        
          

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()