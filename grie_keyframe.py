from math import sin, cos, pi

import time
import lewansoul_lx16a
import serial
import numpy as np
from grie_functions import *
#LX16A.initialize("/dev/cu.usbserial-14310")


#SERIAL_PORT = 'COM9'
SERIAL_PORT = '/dev/ttyUSB0'
controller = lewansoul_lx16a.ServoController(
    serial.Serial(SERIAL_PORT, 115200, timeout=1),
)


# Boot Test Routine
Vlist=[]
for i in range(1,9):
    Voltage=controller.get_voltage(i)
    Vlist.append(Voltage)
Vmax=max(Vlist)
Vmin=min(Vlist)
print(f'Voltage check, min {Vmin}, max {Vmax}')
# Check if battery has sufficient charge
# Check whether motors are connected 
servo_list=[0]
for i in range(1,9):
    try:
        servo=controller.servo(i)
        servo_list.append(servo)
    except:
        print(f'Number{i} servo fails to connect')      
try:
    servo1 = controller.servo(1)
    servo2 = controller.servo(2)
    servo3 = controller.servo(3)
    servo4 = controller.servo(4)

    servo5 = controller.servo(5)
    servo6 = controller.servo(6)
    servo7 = controller.servo(7)
    servo8 = controller.servo(8)
except ServoTimeoutError:
    print("Not Responding .... please reconfigure your servos")
    print("Exiting....")
    exit()



# check the motor initial position
ang0_m5= controller.get_position(5)
ang0_m6= controller.get_position(6)
ang0_m7= controller.get_position(7)
ang0_m8= controller.get_position(8)
ang_67off=ang0_m7-ang0_m6

ang0_m1= controller.get_position(1)
ang0_m2= controller.get_position(2)
ang0_m3= controller.get_position(3)
ang0_m4= controller.get_position(4)
ang_23off=ang0_m3-ang0_m2
print(f'motor 1 inital: {ang0_m1}, motor 5 inital: {ang0_m5}')
print(f'motor 6 inital: {ang0_m6}, motor 2 inital: {ang0_m2}')
print(f'motor 8 inital: {ang0_m8}, motor 4 inital: {ang0_m4}')
print(f'Motor 6&7 has offset of {ang_67off} Degrees')
print(f'Motor 2&3 has offset of {ang_23off} Degrees')

#set safety limit
for i in range(1,9):
    try:
        controller.set_voltage_limits(i,4500,12000)
        controller.set_max_temperature_limit(i,60)
    except:
        print('Motor {i} fails to response')


#this is measure by putting all joint straight and read the position
ang_1_base=674-20
ang_2_base=527
ang_4_base=386

ang_5_base=645-20
ang_6_base=533
ang_8_base=186

Amp=200
t = 0
womiga=3


config1=np.load('captured_frame/config_stand.npy')
config2=np.load('captured_frame/config_lean.npy')
t_req=[0.2,0.5,0.2]
dt=0.01
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
time.sleep(5)











#shutdown routine
servo1.move(ang_1_base)
servo2.move(ang_2_base)
servo3.move(ang_2_base+ang_23off)
servo4.move(ang_4_base)

servo5.move(ang_5_base)
servo6.move(ang_6_base)
servo7.move(ang_6_base+ang_67off)
servo8.move(ang_8_base)

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