from math import sin, cos, pi

import time
import lewansoul_lx16a
import serial
import numpy as np
from grie_functions import *



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


Amp=200
t = 0
womiga=3


config0=np.load('captured_frame/config_stand.npy')
config1=np.load('captured_frame/config_1.npy')
config2=np.load('captured_frame/config_2.npy')
config3=np.load('captured_frame/config_3.npy')
config4=np.load('captured_frame/config_4.npy')
t_req=[0.2,0.5,0.2]
dt=0.01

for mi in range(1,9):
    servo_list[mi].move(config0[mi-1])
time.sleep(2)     
def stepconfig(config1,config2,t_req,dt,servo_list):
    #calculate the path from one config to another
    configpath=trapezoid_path(config1[0],config2[0],t_req,dt)
    for i in range(1,8):
        path=trapezoid_path(config1[i],config2[i],t_req,dt)
        configpath=np.vstack((configpath,path))

    print('configpath.shape',configpath.shape)

    #excute the config transform
    for ti in range(configpath.shape[1]):
        for mi in range(1,9):
            servo_list[mi].move(configpath[mi-1,ti])
        time.sleep(dt)
        #print(ti)

    print('configpath excuted')

t_req=[0.2,0.5,0.2]
stepconfig(config0,config1,t_req,dt,servo_list)
time.sleep(2)
t_req=[0.2,0.2,0.2]
stepconfig(config1,config2,t_req,dt,servo_list)
time.sleep(10)
'''
stepconfig(config2,config3,t_req,dt,servo_list)
time.sleep(1)
stepconfig(config3,config4,t_req,dt,servo_list)
time.sleep(1)
stepconfig(config4,config0,t_req,dt,servo_list)
'''



for mi in range(1,9):
    servo_list[mi].move(config0[mi-1])
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