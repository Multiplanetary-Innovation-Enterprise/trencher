import os
import time
import pigpio
from Peripherals import *
import advpistepper as apis

# motor pin assignments. sv is PWM pin.
sv, fr, brk, rpm, trencher_enable = 12, 27, 22, 17, 23
led_green, led_yellow = 10, 9
x_plus, x_minus, x_step, x_direction = 6, 5, 18, 17 # gantry pins
z_plus, z_minus, z_step, z_direction = 4, 25, 19, 21 # VMS pins
t_plus, t_minus = 16, 20 # bucket ladder direction pins
x_motordrive_enable, z_motordrive_enable = 23, 24

# groupings to help readability later
x_motor_pins = [x_plus, x_minus]
z_motor_pins = [z_plus, z_minus]
t_motor_pins = [t_plus, t_minus]

# constants
MAX_FREQUENCY = 8000
DUTY_CYCLE = 500000

# connect to pigpio
pi = pigpio.pi()

if not pi.connected:
    print("not connected")
    os.system("sudo pigpiod") # need to include "-s2"?
    time.sleep(1)
    pi = pigpio.pi()

# set buttons to pull-up
button_pins = [x_motor_pins, z_motor_pins, t_motor_pins]
for pin in button_pins:
    pi.set_pull_up_down(pin, pigpio.PUD_UP)

# set input pins
input_pins = [x_motor_pins, z_motor_pins, t_motor_pins]
for pin in input_pins:
    pi.set_mode(pin, pigpio.INPUT)

# set output pins
output_pins = [x_motordrive_enable, z_motordrive_enable, x_step, x_direction, z_step, z_direction, led_green, led_yellow]
for pin in output_pins:
    pi.set_mode(pin, pigpio.OUTPUT)

# set initial states. 0 is no output, 1 is positive output
initial_states = {
    x_motordrive_enable: 0,
    z_motordrive_enable: 0,
    x_direction: 1,
    z_plus: 1,
    z_minus: 1,
    led_green: 1,
    led_yellow: 0,
}
for pin, state in initial_states.items():
    pi.write(pin, state)

# accelerates motor using predefined frequencies in GPIO library. 5 microsecond sampling rate.
avail_freq = [100, 160, 200, 250, 320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]
for frequency in avail_freq:
    pi.set_PWM_frequency(z_step, frequency)
    print(pi.get_PWM_frequency(z_step))
    time.sleep(0.1)

# set PWM frequency and duty cycle for z_step
pi.set_PWM_frequency(z_step, MAX_FREQUENCY)
pi.set_PWM_dutycycle(z_step, DUTY_CYCLE)
print(pi.get_PWM_frequency(step))

# main loop
i = 0
while True:
    m = Motor(pi, sv, fr, brk) # motor initialization

    if pi.read(x_plus) == 0: # drives gantry clockwise
        i += 0.01 # does this loop work to accelerate the VMS as well?
        if i > 200:
            pi.hardware_PWM(x_step, 100, DUTY_CYCLE)
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 1)
    elif pi.read(x_minus) == 0: # drives gantry counterclockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 0)
    elif pi.read(z_plus) == 0: # drive VMS clockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 1)
    elif pi.read(z_minus) == 0: # drive VMS counterclockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 0)
    elif pi.read(t_plus) == 0: # drive bucket ladder clockwise
        m.reverse()
        m.setSpeed(100)
    elif pi.read(t_minus) == 0: # drive bucket ladder counterclockwise
        m.forward()
        m.setSpeed(100)
    else:
        m.setSpeed(0)
        pi.write(z_motordrive_enable, 0)
        pi.write(x_motordrive_enable, 0)