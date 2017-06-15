import struct
import subprocess
import os.path

def convertToPWM(angle,throttle,conf):
    angle = max(-0.5, angle)
    angle = min(0.5, angle)

    throttle = max(0, throttle)
    throttle = min(1, throttle)

    angle_pwm    = (angle)*(conf['max_angle_pwm'] - conf['min_angle_pwm']) +  conf['mid_angle_pwm']
    throttle_pwm = throttle * (conf['max_throttle_pwm'] - conf['min_throttle_pwm'])  + conf['min_throttle_pwm']

    return(angle_pwm, throttle_pwm)

def convertFromPWM(angle_pwm, throttle_pwm, conf):
    throttle = (float(throttle_pwm)-conf['min_throttle_pwm'])/float(conf['max_throttle_pwm'] - conf['min_throttle_pwm'])
    angle = (float(angle_pwm) - conf['mid_angle_pwm'] )/float(conf['max_angle_pwm'] - conf['min_angle_pwm'])  
    return(angle,throttle)

def sendToArduino(ser,angle,throttle):
    dataToSend = struct.pack('<BBhh', ord('A'), ord('A'),int(angle),int(throttle))
    #ser.write('AA'.encode())
    ser.write(dataToSend)


def ismounted():
    '''checks if USB_AI_RC_Car_Stick is mounted'''
    vpath = "/home/pi/record"
    return(os.path.ismount(vpath))


def mount():
    '''mounts USB_AI_RC_Car_Stick'''
    vpath = "/home/pi/record"
    if not ismounted():
        cmd = 'sudo mount /dev/sda1 ' + vpath
        proc = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE).stdout.read()
        print(proc)
    else:
        print("Was already mounted, skipping")

def umount():
    '''unmounts USB_AI_RC_Car_Stick'''
    vpath = "/home/pi/record"
    if ismounted():
        cmd = 'sudo umount ' + vpath
        proc = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE).stdout.read()
        print(proc)
    else:
        print("Not mounted, skipping")
