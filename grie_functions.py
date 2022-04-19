import numpy as np
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