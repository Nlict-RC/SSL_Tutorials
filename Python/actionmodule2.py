# -*- coding: utf-8 -*-
"""
@Brief: This is an action module to control ZJUNlict's robots
@Version: ZJUNlict Communication Protocol 1.6
@author: Wang Yunkai
"""

import serial
import struct
from time import sleep

ACTION_IP = '10.12.225.78'
ACTION_PORT = 1030

class ActionModule:
    def __init__(self, COM='COM5'):
        self.serial = serial.Serial(COM, 115200)
    
    def send_action(self, robot_num=0, vx=0, vy=0, w=0):
        # m/s -> cm/s, rad/s -> 1/40 rad/s
        vx = int(100 * vx)
        vy = int(100 * vy)
        w  = int(w * 40)

        send_package = [b'\x00' for i in range(25)]
        send_package[0] = b'\x48'
        send_package[1] = struct.pack('!B', robot_num)
        sign_vx = 0 if vx >= 0 else 1
        sign_vy = 0 if vy >= 0 else 1
        sign_w  = 0 if w  >= 0 else 1
        send_package[2] = struct.pack('!B', sign_vx*128 + abs(vx)%128)
        send_package[3] = struct.pack('!B', sign_vy*128 + abs(vy)%128)
        send_package[4] = struct.pack('!B', sign_w *128 + abs(w )%128)
        send_package[17] = struct.pack('!B',int(abs(w)/128) + int(abs(vy)/128)*16 + int(abs(vx)/128)*64)
        package = struct.pack('!25c', send_package[0],send_package[1],send_package[2],send_package[3],send_package[4],send_package[5],send_package[6],send_package[7],send_package[8],send_package[9],send_package[10],send_package[11],send_package[12],send_package[13],send_package[14],send_package[15],send_package[16],send_package[17],send_package[18],send_package[19],send_package[20],send_package[21],send_package[22],send_package[23],send_package[24])
        #print(package)
        self.serial.write(package)
        
    def close(self):
        self.serial.close()
        
if __name__ == "__main__":
    action = ActionModule('COM5')
    while(True):
        action.send_action(robot_num=5, vx=0, vy=0, w=3)
        sleep(0.015)