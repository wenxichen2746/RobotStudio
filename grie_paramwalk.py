import numpy as np
import time 

from math import sin
import math


from grie_motorcontrol import mcontroller
from grie_functions import *

param=np.load('bestparam_hc0504.npy',allow_pickle='TRUE').item()
param={'amp': [ 0.64119211, -0.29115442,  0.82053762],\
     'phase': [2.2515711 , 0.33513259, 0.70721696],\
          'devia': [-0.01431187,  0.28189022, -0.01911612],\
               'womiga': 20}


c=mcontroller()
c.bootcheck()

tlimit=10
t=0

while t<tlimit:
    actionarray_m8=param2action_m8(param,t)
    actionarray=actionarray*1000/(1.33*np.pi)
    commandarray=actionarray+c.config_stand
    for mi in range(1,9):
        c.servo_list[mi].move(actionarray[mi-1])
    t+=0.01
    time.sleep(0.01)





c.shutdown()