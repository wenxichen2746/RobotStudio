import numpy as np
import time 
import lewansoul_lx16a
import serial
from math import sin
import math

from grie_functions import *

#param=np.load('bestparam_hc0504.npy',allow_pickle='TRUE').item()

param={'amp': [ 0.16746452, -0.20691382, -0.06519423],\
       'phase': [4188.479158445201, 4140.7734509332095, 4206.896595629934],\
       'devia': [-0.009991  ,  0.03, -0.00872341], 'womiga': 3.578031868698937}
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

tlimit=15
t=0
config_stand=np.load('captured_frame/config_stand.npy')
for mi in range(1,9):
    servo_list[mi].move(config_stand[mi-1])
time.sleep(2)
while t<tlimit:
    actionarray_m8=param2action_m8(param,t)
    actionarray_m8=actionarray_m8*1000/(0.66*np.pi)
    commandarray=actionarray_m8+config_stand
    for mi in range(1,9):
        servo_list[mi].move(commandarray[mi-1])
    t+=0.01
    time.sleep(0.01)




#shutdown routine
for mi in range(1,9):
    servo_list[mi].move(config_stand[mi-1])

time.sleep(0.5)
Vlist=[]
for i in range(1,9):
    Voltage=controller.get_voltage(i)
    Vlist.append(Voltage)
Vmax=max(Vlist)
Vmin=min(Vlist)
print(f'Voltage check, min {Vmin}, max {Vmax}')#voltage check
'''
for i in range(1,9):
    controller.motor_off(i)

print(f'Machine Shutting down')
'''