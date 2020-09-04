# coding: utf-8

import RPi.GPIO as GPIO
import time
import atexit
import socket


atexit.register(GPIO.cleanup)
#GPIO.cleanup()
servopin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin,50)
p.start(0)
#time.sleep(0.6)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(5)

def new_rotate(tms):
        #改变占功比，让舵机旋转
    p.ChangeDutyCycle(6.25)
    time.sleep(0.1)#停止一个周期
    #p.ChangeDutyCycle(0)#把占功比改成0，防止抖动
    time.sleep(tms)  #停止一段时间t
    print '正在下压'
    p.ChangeDutyCycle(5)#改变占功比，让舵机旋转
    #print '停止'
    time.sleep(0.1)#停止一个周期
    p.ChangeDutyCycle(0)#把占功比改成0，防止抖动
    time.sleep(1)
    #print '开始:'

def main():
    while True:
        sock, addr = s.accept()
        t = sock.recv(1024)
        t = t.decode('utf-8')
        print("press:  "+t+"ms")
        new_rotate(float(t)/1000)


if __name__ == "__main__":
    main()
    #while True:
        #new_rotate(0.8)
