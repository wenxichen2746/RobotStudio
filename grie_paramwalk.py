import numpy as np
import time 
import lewansoul_lx16a
import serial
from math import sin
import math


from grie_motorcontrol import mcontroller
from grie_functions import *

param=np.load('bestparam_hc0504.npy',allow_pickle='TRUE').item()
param={'amp': [ 0.64119211, -0.29115442,  0.82053762],\
     'phase': [2.2515711 , 0.33513259, 0.70721696],\
          'devia': [-0.01431187,  0.28189022, -0.01911612],\
               'womiga': 20}

SERIAL_PORT = '/dev/ttyUSB0'
controller=lewansoul_lx16a.ServoController(
            serial.Serial(SERIAL_PORT, 115200, timeout=1),
            )
servo_list=[0]
for i in range(1,9):
    try:
        servo=controller.servo(i)
        servo_list.append(servo)
    except:
        print(f'Number{i} servo fails to connect') 

tlimit=10
t=0
config_stand=np.load('captured_frame/config_stand.npy')

while t<tlimit:
    actionarray_m8=param2action_m8(param,t)
    actionarray=actionarray*1000/(1.33*np.pi)
    commandarray=actionarray+config_stand
    for mi in range(1,9):
        c.servo_list[mi].move(actionarray[mi-1])
    t+=0.01
    time.sleep(0.01)




#shutdown routine
for mi in range(1,9):
    servo_list[mi].move(config_stand[mi-1])


Vlist=[]
for i in range(1,9):
    Voltage=controller.get_voltage(i)
    Vlist.append(Voltage)
Vmax=max(Vlist)
Vmin=min(Vlist)
print(f'Voltage check, min {Vmin}, max {Vmax}')#voltage check

for i in range(1,9):
    controller.motor_off(i)

print(f'Machine Shutting down')