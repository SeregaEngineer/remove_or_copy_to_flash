import os
import pyudev
import subprocess

import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) # берем название GPIO которое

red = 2
blue = 3
green = 4

GPIO.setup(red, GPIO.OUT) 
GPIO.setup(blue, GPIO.OUT) 
GPIO.setup(green, GPIO.OUT) 
  


path_mount = "/media/usb/"

def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    #monitor.filter_by(subsystem='usb')
    monitor.filter_by('block')




    for device in iter(monitor.poll, None):
        if 'ID_FS_TYPE' in device:
            if device.action == 'add':
                print('{0} partition {1} with dev name {2}' .format(device.action, device.get('ID_FS_LABEL'), device.parent.device_node))
                GPIO.output(red, False) 
                GPIO.output(green, False)
                GPIO.output(blue, True) 
               # try:
               #     subprocess.run(['mkfs.vfat', device.parent.device_node + '1'])
               #     print('mkfs.vfat', device.parent.device_node + '1')
               # except:
                subprocess.run(['mkfs.vfat', device.parent.device_node])
                print('mkfs.vfat', device.parent.device_node)
                GPIO.output(green, True)
                GPIO.output(blue, False) 
           #print(f"mount {device.parent.device_node} {path_mount}")
                print("Clear")
           # subprocess.run(['mount', device.parent.device_node + '1', path_mount])

if __name__ == '__main__':
    main()
