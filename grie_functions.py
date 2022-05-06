import numpy as np
from math import sin
def trapezoid_path(ang1,ang2,t_req,dt):


    t_acce=t_req[0]
    t_slow=t_req[1]
    t_mid=t_req[2]
    vmax=(ang2-ang1)/(0.5*t_acce+t_mid+0.5*t_slow)
    ang=[ang1]
    v=[0]

    dt=0.01
    t=0

    while t<t_acce:
        new_v=v[-1]+dt*vmax/t_acce
        v.append(new_v)
        new_ang=ang[-1]+(v[-1]+v[-2])/2*dt
        ang.append(new_ang)
        t+=dt

    while t<t_acce+t_mid:
        v.append(v[-1])
        new_ang=ang[-1]+(v[-1]+v[-2])/2*dt
        ang.append(new_ang) 
        t+=dt

    while t<t_acce+t_mid+t_slow:
        new_v=v[-1]-dt*vmax/t_slow
        v.append(new_v)
        new_ang=ang[-1]+(v[-1]+v[-2])/2*dt
        ang.append(new_ang)
        t+=dt
    return ang

    
def param2action(param,t):
    actionarray=np.zeros((6))
    amp=param['amp']
    phase=param['phase']
    devia=param['devia']
    womiga=param['womiga']
    for i in range(3):
        actionarray[i]=amp[i]*sin(womiga*t+phase[i])+devia[i]
    actionarray[3]=amp[0]*sin(womiga*t+phase[0])+devia[0]
    #both hip acting same
    for i in range(1,3):
        actionarray[i+3]=amp[i]*sin(womiga*t+phase[i]+np.pi)+devia[i]
    #two leg act in opposite phase
    return actionarray

def param2action_m8(param,t):
    actionarray=np.zeros((8))
    amp=param['amp']
    phase=param['phase']
    devia=param['devia']
    womiga=param['womiga']

    actionarray[0]=amp[0]*sin(womiga*t+phase[0])+devia[0]
    actionarray[1]=amp[1]*sin(womiga*t+phase[1])+devia[1]
    actionarray[2]=amp[1]*sin(womiga*t+phase[1])+devia[1]
    actionarray[3]=amp[2]*sin(womiga*t+phase[2])+devia[1]

    actionarray[4]=amp[0]*sin(womiga*t+phase[0])+devia[0]
    actionarray[5]=-amp[1]*sin(womiga*t+phase[1])+devia[1]
    actionarray[6]=-amp[1]*sin(womiga*t+phase[1])+devia[1]
    actionarray[7]=-amp[2]*sin(womiga*t+phase[2])+devia[1]
