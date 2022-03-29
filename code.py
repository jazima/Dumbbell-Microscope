'''
Team Dumbell Stepper Driver with Serial Communication
'''

import board
import time
import digitalio
import usb_cdc

# Global variables
delay = 1 #delay between steps of the stepper motor in seconds

#################################################################
#                   Serial Communication Protocol               #
#################################################################
"""
All signals are sent in bytes
A single signal consists of 3 bytes, the first indicating the axis of movement
the second indicating the direction of adjustment, and the third indicating the
number of steps
"""
motor_axes = {
    "x": int(0).to_bytes(1, "big"),
    "y": int(1).to_bytes(1, "big"),
    "focus_fine": int(2).to_bytes(1, "big"),
    "focus_coarse": int(3).to_bytes(1, "big")
}

#steps are given as an integer
#direction is given as a bool
#################################################################
#                 End Serial Communication Protocol             #
#################################################################

# Usb serial initialize
uart = usb_cdc.data

# Variable Definition of GPIO Pins
x_dir_pin = board.GP15  ################## ENTER GPIO PIN ###################
x_step_pin = board.GP14    ################## ENTER GPIO PIN ###################
y_dir_pin = board.GP13   ################## ENTER GPIO PIN ###################
y_step_pin = board.GP12   ################## ENTER GPIO PIN ###################
fine_dir_pin = board.GP11 ################## ENTER GPIO PIN ###################
fine_step_pin = board.GP10################## ENTER GPIO PIN ###################
coarse_dir_pin = board.GP16 ################## ENTER GPIO PIN ###################
coarse_step_pin = board.GP17 ################## ENTER GPIO PIN ###################
enable_pin = board.GP9  ################## ENTER GPIO PIN ###################

# Set up input pins for stepper motor
x_dir = digitalio.DigitalInOut(x_dir_pin)
x_dir.direction = digitalio.Direction.OUTPUT

x_step = digitalio.DigitalInOut(x_step_pin)
x_step.direction = digitalio.Direction.OUTPUT

y_dir = digitalio.DigitalInOut(y_dir_pin)
y_dir.direction = digitalio.Direction.OUTPUT

y_step = digitalio.DigitalInOut(y_step_pin)
y_step.direction = digitalio.Direction.OUTPUT

fine_dir = digitalio.DigitalInOut(fine_dir_pin)
fine_dir.direction = digitalio.Direction.OUTPUT

fine_step = digitalio.DigitalInOut(fine_step_pin)
fine_step.direction = digitalio.Direction.OUTPUT

coarse_dir = digitalio.DigitalInOut(coarse_dir_pin)
coarse_dir.direction = digitalio.Direction.OUTPUT

coarse_step = digitalio.DigitalInOut(coarse_step_pin)
coarse_step.direction = digitalio.Direction.OUTPUT

enable = digitalio.DigitalInOut(enable_pin)
enable.direction = digitalio.Direction.OUTPUT

def step_motor(dir_pin: digitalio.DigitalInOut, step_pin:digitalio.DigitalInOut, steps:int, direction:bool) -> None:
    """Moves the specified motor by the given number of steps in the given direction.

    :dir_pin: the pin corresponding to the direction of rotation of the specified motor.
    :step_pin: the pin corresponding to the step of the specified motor
    :steps: an integer number of steps to be taken by the specified motor
    :direction: boolean indicating the direction.
    :returns: None
    """
    dir_pin.value = direction
    enable.value = False
    for step in range(steps):
        step_pin.value = True
        time.sleep(delay)
        step_pin_pin.value = False
        time.sleep(delay)
    enable.value = True
    return

def receive_signal():
    """Receives and decodes the incoming serial signal

    :returns: tuple with the decoded signal
    """
    while uart.in_waiting < 3: #wait for serial input
        continue

    axis = uart.read(1)
    direction = int.from_bytes(uart.read(1), "big")
    steps = int.from_bytes(uart.read(1), "big")

    #decode the axis
    if(axis == motor_axes["x"]):
        dir_pin = x_dir
        step_pin = x_step
    elif(axis == motor_axes["y"]):
        dir_pin = y_dir
        step_pin = y_step
    elif(axis == motor_axes["focus_fine"]):
        dir_pin = fine_dir
        step_pin = fine_step
    elif(axis == motor_axes["focus_coarse"]):
        dir_pin = coarse_dir
        step_pin = coarse_step

    return(dir_pin, step_pin, direction, steps)

enable.value = True
while True:
    dir_pin, step_pin, direction, steps = receive_signal()
    step_motor(dir_pin, step_pin, steps, direction)
