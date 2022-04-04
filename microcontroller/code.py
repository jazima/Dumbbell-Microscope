'''
    Stepper driver for Team Dumbbell malaria microscopy widget.
    Copyright (C) 2022 Jazim Akbar, Nidal Danial, Saeed Jan, Henry Prickett-Morgan, and Iliya Shofman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import board
import time
import digitalio
import usb_cdc

# Global variables
step_delay = 0.002  # Delay between steps of the stepper motor in seconds
enable_delay = 0.005

#################################################################
#                   Serial Communication Protocol               #
#################################################################
'''
All signals are sent in bytes
A single signal consists of 3 bytes, the first indicating the axis of movement
the second indicating the direction of adjustment, and the third indicating the
number of steps
'''

# steps are given as an integer
# direction is given as a bool
#################################################################
#                 End Serial Communication Protocol             #
#################################################################

# Usb serial initialize
uart = usb_cdc.data

# Variable Definition of GPIO Pins
x_dir_pin = board.GP15
x_step_pin = board.GP14
x_en_pin = board.GP13

y_dir_pin = board.GP12
y_step_pin = board.GP11
y_en_pin = board.GP10

fine_dir_pin = board.GP9
fine_step_pin = board.GP8
fine_en_pin = board.GP7

coarse_en_pin = board.GP6


# Set up input pins for stepper motor
x_dir = digitalio.DigitalInOut(x_dir_pin)
x_dir.direction = digitalio.Direction.OUTPUT
x_step = digitalio.DigitalInOut(x_step_pin)
x_step.direction = digitalio.Direction.OUTPUT
x_enable = digitalio.DigitalInOut(x_en_pin)
x_enable.direction = digitalio.Direction.OUTPUT

y_dir = digitalio.DigitalInOut(y_dir_pin)
y_dir.direction = digitalio.Direction.OUTPUT
y_step = digitalio.DigitalInOut(y_step_pin)
y_step.direction = digitalio.Direction.OUTPUT
y_enable = digitalio.DigitalInOut(y_en_pin)
y_enable.direction = digitalio.Direction.OUTPUT

fine_dir = digitalio.DigitalInOut(fine_dir_pin)
fine_dir.direction = digitalio.Direction.OUTPUT
fine_step = digitalio.DigitalInOut(fine_step_pin)
fine_step.direction = digitalio.Direction.OUTPUT
fine_enable = digitalio.DigitalInOut(fine_en_pin)
fine_enable.direction = digitalio.Direction.OUTPUT

coarse_enable = digitalio.DigitalInOut(coarse_en_pin)
coarse_enable.direction = digitalio.Direction.OUTPUT


motor_axes = {
    0: (x_dir, x_step, x_enable),
    1: (y_dir, y_step, y_enable),
    2: (fine_dir, fine_step, fine_enable),
    3: coarse_enable
}

def step_motor(dir: digitalio.DigitalInOut, step: digitalio.DigitalInOut, 
enable: digitalio.DigitalInOut, steps: int, direction: bool) -> None:
    '''Moves the specified motor by the given number of steps in the given direction.

    :dir_pin: the pin corresponding to the direction of rotation of the specified motor.
    :step_pin: the pin corresponding to the step of the specified motor
    :steps: an integer number of steps to be taken by the specified motor
    :direction: boolean indicating the direction.
    :returns: None
    '''
    dir.value = direction
    enable.value = False
    time.sleep(enable_delay)
    for i in range(steps):
        step.value = True
        time.sleep(step_delay)
        step.value = False
        time.sleep(step_delay)
    enable.value = True
    return


def receive_signal():
    '''Receives and decodes the incoming serial signal

    :returns: tuple with the decoded signal
    '''
    while uart.in_waiting < 3:  # Wait for serial input
        continue

    axis = int.from_bytes(uart.read(1), "big")
    direction = int.from_bytes(uart.read(1), "big")
    steps = int.from_bytes(uart.read(1), "big")

    # Decode the axis
    dir, step, enable = motor_axes[axis]

    return(dir, step, enable, direction, steps)


x_enable.value = True
y_enable.value = True
fine_enable.value = True
while True:
    dir, step, enable, direction, steps = receive_signal()
    step_motor(dir, step, enable, steps, direction)
    uart.write(int(0).to_bytes(1, "big"))