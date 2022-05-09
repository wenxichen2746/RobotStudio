from math import sin, cos, pi

import time
import lewansoul_lx16a
import serial
import numpy as np
from grie_functions import *
import scipy.interpolate as interpolate


from grie_functions import *



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


#this is measure by putting all joint straight and read the position



config_num=4
dt=0.01
tmax=10

configM=np.empty(8)
for i in range(0,config_num):
    filename='captured_frame/config_'+str(i)+'.npy'
    config=np.load(filename)
    configM=np.vstack((configM,config))
    
tf=np.linspace(0,tmax,configM.shape[0])
ti=np.arange(0,tmax,dt)
configpath=np.empty(ti.shape[0])
for mi in range(8):
    #f=interpolate.interp1d(tf,configM[:,mi])
    f=interpolate.BarycentricInterpolator(tf,configM[:,mi])
    path=f(ti)
    configpath=np.vstack((configpath,path))
configpath=np.delete(configpath,0,axis=0)

#conduct move
for ti in range(configpath.shape[1]):
    for mi in range(1,9):
        servo_list[mi].move(configpath[mi-1,ti])
    time.sleep(dt)

time.sleep(4)

for mi in range(1,9):
    servo_list[mi].move(configM[0,mi-1])
time.sleep(1)

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