import os
import pyudev
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


src = "/home/sergey/test/"


def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    #monitor.filter_by(subsystem='usb')
    monitor.filter_by('block')

    try:
        for device in iter(monitor.poll, None):
            if 'ID_FS_TYPE' in device:
                if device.action == 'add':
                    GPIO.output(red, False) 
                    GPIO.output(green, False)
                    GPIO.output(blue, False) 

                    print('{0} partition {1} with dev name {2}' .format(device.action, device.get('ID_FS_LABEL'), device.parent.device_node))
                    GPIO.output(blue, True) 
                    os.system(f'mount {device.parent.device_node}1 {path_mount}')
                    print("mount")
                    os.system(f'cp -r  {src}  {path_mount}')
                    print("copy finall")
                    os.system(f'umount {path_mount}')
                    
                    GPIO.output(blue, False) 
                    GPIO.output(green, True) 
                    print("unmoun flash")

    except:
        #print(ex)
        GPIO.output(green, False)
        GPIO.output(blue, False) 
        GPIO.output(red, True) 

    finally:
        print("finall")
        GPIO.output(green, False)
        GPIO.output(blue, False) 
        GPIO.output(red, True) 

if __name__ == '__main__':
    main()