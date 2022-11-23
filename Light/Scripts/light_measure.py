from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/b03-203/Desktop/SM_Lab/HeatingLamp_blue.jpg')
camera.stop_preview()