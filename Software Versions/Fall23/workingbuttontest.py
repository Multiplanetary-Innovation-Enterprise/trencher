import os
import time
import pigpio
from Peripherals import *

#os.system("sudo pigpiod")

pi = pigpio.pi()

os.system("sudo killall pigpiod")

if not pi.connected:
    #print("not connected")
    os.system("sudo pigpiod -s2 -t0") #restarts the pigpio daemon, changes smapling rate to 2 and debugs waveform function
    time.sleep(1)
    pi = pigpio.pi()

#****************************
# Trencher motor controller pinout
sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
trencher_Enable = 23
#****************************

led_green = 10 
led_yellow = 9

# gantry buttons
x_plus = 6
x_minus = 5

# vms buttons
z_plus = 4
z_minus = 25

# bucket ladder directions
t_plus = 16 #forward
t_minus = 20 #backward

x_motordrive_enable = 23
z_motordrive_enable = 24

# step is speed pin
x_step = 18
x_direction = 17

# step = speed pin
z_step = 19
z_direction = 21

#pull-up pull down sets buttons to output/input, PUD up tells the program to check when the circuit going through the buttons is broken.

pi.set_pull_up_down(20, pigpio.PUD_UP) #backwards bucket ladder
 #forwards bucket ladder
pi.set_mode(22, pigpio.OUTPUT) #sets up enable pin for output
pi.set_mode(12, pigpio.OUTPUT) #sets up speed pin for output
pi.set_mode(27, pigpio.OUTPUT) #sets up direction pin for output

pi.set_pull_up_down(z_minus, pigpio.PUD_UP) #VMS down
pi.set_pull_up_down(z_plus, pigpio.PUD_UP) #VMS up

pi.set_pull_up_down(16, pigpio.PUD_UP)

pi.set_pull_up_down(x_plus, pigpio.PUD_UP) #gantry right
pi.set_pull_up_down(x_minus, pigpio.PUD_UP) #gantry left

#pi.set_pull_up_down(22, pigpio.PUD_UP)

pi.set_mode(4, pigpio.INPUT) 
pi.set_mode(20, pigpio.INPUT)
pi.set_mode(25, pigpio.INPUT)
pi.set_mode(16, pigpio.INPUT) 

#pigpio.INPUT sets the program to read an input

pi.set_mode(x_plus, pigpio.INPUT)
pi.set_mode(x_minus, pigpio.INPUT)

pi.set_mode(z_plus, pigpio.INPUT)
pi.set_mode(z_minus, pigpio.INPUT)

pi.set_mode(t_plus, pigpio.INPUT)
pi.set_mode(t_minus, pigpio.INPUT)

#pigpio.OUTPUT sets the program to output a signal

pi.set_mode(x_motordrive_enable, pigpio.OUTPUT)
pi.set_mode(z_motordrive_enable, pigpio.OUTPUT)

pi.set_mode(x_step, pigpio.OUTPUT)
pi.set_mode(x_direction, pigpio.OUTPUT)
pi.set_mode(z_step, pigpio.OUTPUT)
pi.set_mode(z_direction, pigpio.OUTPUT)

pi.set_mode(led_green, pigpio.OUTPUT)
pi.set_mode(led_yellow, pigpio.OUTPUT)

#pi.set_mode(22, pigpio.OUTPUT)

#pi.set_mode(sv, pigpio.OUTPUT)
#pi.set_mode(fr, pigpio.OUTPUT)

# sets no output, akin to setting defaults. 0 is no output

pi.write(x_motordrive_enable, 0)
pi.write(z_motordrive_enable, 0)

# sets default to output. 1 is positive output

pi.write(x_direction, 1)
pi.write(z_plus, 1)
pi.write(z_minus, 1)

pi.write(t_plus, 1)
pi.write(t_plus, 1)

pi.write(led_green, 1)
pi.write(led_yellow, 0)
    
m = Motor(pi, sv, fr, brk)

# sets the frequency and duty cycle for the gantry (x) and vms motors (z)
#global gantry_freq
#global vms_freq
#gantry_freq = 0
#vms_freq = 0

pi.write(brk, 0) #switched bucket ladder to run high
#pi.write(23, 1) #gantry pin was spamming on electronic saloon

avail_freq = [100, 160, 200, 250, 320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]

#pi.set_PWM_dutycycle(z_step, 128)


#c = 0
#while c<12:
    #pi.set_PWM_frequency(z_step, avail_freq[c])
    #print(pi.get_PWM_frequency(z_step))
    #time.sleep(.1)
    #c+=1

#pi.set_PWM_frequency(z_step, 8000)
#print(pi.get_PWM_frequency(step))

        

#def accel_curve(value, motor):
    #gantry_freq = 0
    #if motor == 'x':
        
        #if value >= 800:
            #gantry_freq = 8000
        #else:
            #gantry_freq = value*10 
    
        #for key in avail_freq.keys():
            #if value == key:
                #gantry_freq = avail_freq[key]
                
        #pi.set_PWM_frequency(x_step, gantry_freq)
    #elif motor == 'z':
        #if value >= 300:
            #vms_freq = 3000
        #else:
            #vms_freq = value*10
        #pi.set_PWM_frequency(z_step, vms_freq)


n = 0
i = 0
#switch1 = False
#switch2 = False

#code below starts the infinite loop which allows all three devices to run (gantry, bucket ladder, VMS)
while True:

    speed = 0 #variable for frequency for BLDC
    duty = 0 #variable for duty cycle for BLDC
    print(f"BLDC Speed: {(speed)}")
    print(f"BLDC Duty: {(duty)}")
    #print(f"Enable:")

    #code for the gantry starts below and runs from lines 185-207
    if pi.read(x_plus) == 0: # drives the gantry clockwise
        #i+=0.01
        #if i > 200:
            #pi.hardware_PWM(x_step, 100, 500000)
        #accel_curve(i,'x')
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 1)
        pi.set_PWM_dutycycle(x_step, 128)
        pi.set_PWM_frequency(x_step, 1000)

       
        #print(f"x_plus: {i} gantry frequency: {pi.get_PWM_frequency(x_step)}")
        
    elif pi.read(x_minus) == 0:# drives the gantry counterclockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 0)
        pi.set_PWM_dutycycle(x_step, 128)
        pi.set_PWM_frequency(x_step, 1000)

    else:
        pi.write(x_motordrive_enable, 0)
        
        #print(f"x_minus: {i} gantry frequency: {pi.get_PWM_frequency(x_step)}")
    
    #code for the VMS starts below and runs from lines 210-226
    if pi.read(z_plus) == 0: # runs the vms clockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 1)
        pi.set_PWM_dutycycle(z_step, 128)
        pi.set_PWM_frequency(z_step, 2500)
        
        #print(f"z_plus: {i} vms frequency: {pi.get_PWM_frequency(z_step)}")
    elif pi.read(z_minus) == 0: # runs the vms counterclockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 0)
        pi.set_PWM_dutycycle(z_step, 128)
        pi.set_PWM_frequency(z_step, 2500)

    else:
        pi.write(z_motordrive_enable, 0)
        
        #print(f"z_minus: {i} vms frequency: {pi.get_PWM_frequency(z_step)}")

    #code for the bucekt ladder starts below and runs from lines 229-255
    if pi.read(t_plus) == 0:
        pi.write(22, 1)
        speed = speed + 500
        duty = duty + 128
        pi.set_PWM_frequency(12, speed) #12 is the only PWM pin, so iy needs this function rather than just writing
        pi.set_PWM_dutycycle(12, duty)
        pi.write(fr, 1)
        print(f"Duty:{(duty)}")
        print(f"Speed:{(speed)}")
        #m.reverse()
        #m.setSpeed(100)
        print("t_plus")
    elif pi.read(t_minus) == 0:
        pi.write(22, 1)
        speed = speed + 500
        duty = duty + 128
        pi.set_PWM_frequency(12, speed)
        pi.set_PWM_dutycycle(12, duty)
        pi.write(fr, 0)
        print(f"Duty:{(duty)}")
        print(f"Speed:{(speed)}")
        #m.forward()
        #m.setSpeed(100)
        print("t_minus")
    else:
        m.setSpeed(0)
        pi.write(22, 0)

    #if switch 1 is set to true
        #do the instructions for bucket ladder
        #Either go backwards or forwards depending on which button is pressed
    #if switch 2 is set to true
        #do the instructions for the gantry
        #Either go left or right depending on which button is pressed

    #Pseudocode for this since I still don't fully understand if I understand
    #The switch logic correctly
