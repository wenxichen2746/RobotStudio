from math import sin, cos, pi

import time
import lewansoul_lx16a
import serial
import numpy as np
from grie_functions import *


from grie_motorcontrol import mcontroller
from grie_functions import *



c=mcontroller()
c.bootcheck()



#this is measure by putting all joint straight and read the position


Amp=200
t = 0
womiga=3


config1=np.load('captured_frame/config_stand.npy')
config2=np.load('captured_frame/config_lean.npy')
t_req=[0.2,0.5,0.2]
dt=0.01

def stepconfig(config1,config2,t_req,dt,servo_list):
    #calculate the path from one config to another
    configpath=trapezoid_path(config1[0],config2[0],t_req,dt)
    for i in range(1,8):
        path=trapezoid_path(config1[0],config2[0],t_req,dt)
        configpath=np.vstack((configpath,path))

    print('configpath.shape',configpath.shape)

    #excute the config transform
    for ti in range(configpath.shape[1]):
        for mi in range(1,9):
            servo_list[mi].move(configpath[mi-1,ti])
        time.sleep(dt)
        #print(ti)

    print('configpath excuted')

    
stepconfig(config1,config2,t_req,dt,c.servo_list)
time.sleep(5)


c.shutdown()