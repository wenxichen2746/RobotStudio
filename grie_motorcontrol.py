from math import sin, cos, pi

import time
import lewansoul_lx16a
import serial
import numpy as np
from grie_functions import *

class mcontroller:
    def __init__(self,pi=True) -> None:
        if pi==True:
            SERIAL_PORT = '/dev/ttyUSB0'
        else:
            SERIAL_PORT = 'COM9'
        self.controller=lewansoul_lx16a.ServoController(
            serial.Serial(SERIAL_PORT, 115200, timeout=1),
            )
        self.servo_list=self.bootcheck()
        self.config_stand=np.load('captured_frame/config_stand.npy')
       


    def bootcheck(self):     
        # Boot Test Routine
        Vlist=[]
        for i in range(1,9):
            Voltage=self.controller.get_voltage(i)
            Vlist.append(Voltage)
        Vmax=max(Vlist)
        Vmin=min(Vlist)
        print(f'Voltage check, min {Vmin}, max {Vmax}')
        # Check if battery has sufficient charge
        # Check whether motors are connected 
        servo_list=[0]
        for i in range(1,9):
            try:
                servo=self.controller.servo(i)
                servo_list.append(servo)
            except:
                print(f'Number{i} servo fails to connect')      


        for i in range(1,9):
            try:
                self.controller.set_voltage_limits(i,4500,12000)
                self.controller.set_max_temperature_limit(i,60)
            except:
                print('Motor {i} fails to response')

        return servo_list

    def initalpos(self):
        anglist=[]
        for mi in range(1,9):
            ang=self.controller.get_position(mi)
            anglist.append(ang)
        print(f'motor 1 inital: {anglist[0]}, motor 5 inital: {anglist[4]}')
        print(f'motor 2 inital: {anglist[1]}, motor 6 inital: {anglist[5]}')
        print(f'motor 4 inital: {anglist[3]}, motor 8 inital: {anglist[7]}')
        print(f'Motor 6&7 has offset of {anglist[5]-anglist[6]} Degrees')
        print(f'Motor 2&3 has offset of {anglist[1]-anglist[2]} Degrees')

    def shutdown(self):
        #shutdown routine
        for mi in range(1,9):
            self.servo_list[mi].move(self.config_stand[mi-1])


        Vlist=[]
        for i in range(1,9):
            Voltage=self.controller.get_voltage(i)
            Vlist.append(Voltage)
        Vmax=max(Vlist)
        Vmin=min(Vlist)
        print(f'Voltage check, min {Vmin}, max {Vmax}')#voltage check

        for i in range(1,9):
            self.controller.motor_off(i)

        print(f'Machine Shutting down')