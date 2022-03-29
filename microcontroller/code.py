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
delay = 1  # Delay between steps of the stepper motor in seconds

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
y_dir_pin = board.GP13
y_step_pin = board.GP12
fine_dir_pin = board.GP11
fine_step_pin = board.GP10
coarse_dir_pin = board.GP16
coarse_step_pin = board.GP17
enable_pin = board.GP9

motor_axes = {
    0: (x_dir_pin, x_step_pin),
    1: (y_dir_pin, y_step_pin),
    2: (fine_dir_pin, fine_step_pin),
    3: (coarse_dir_pin, coarse_step_pin)
}

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


def step_motor(dir_pin: digitalio.DigitalInOut, step_pin: digitalio.DigitalInOut, steps: int, direction: bool) -> None:
    '''Moves the specified motor by the given number of steps in the given direction.

    :dir_pin: the pin corresponding to the direction of rotation of the specified motor.
    :step_pin: the pin corresponding to the step of the specified motor
    :steps: an integer number of steps to be taken by the specified motor
    :direction: boolean indicating the direction.
    :returns: None
    '''
    dir_pin.value = direction
    enable.value = False
    for step in range(steps):
        step_pin.value = True
        time.sleep(delay)
        step_pin.value = False
        time.sleep(delay)
    enable.value = True
    return


def receive_signal():
    '''Receives and decodes the incoming serial signal

    :returns: tuple with the decoded signal
    '''
    while uart.in_waiting < 3:  # Wait for serial input
        continue

    axis = uart.read(1)
    direction = int.from_bytes(uart.read(1), "big")
    steps = int.from_bytes(uart.read(1), "big")

    # Decode the axis
    dir_pin, step_pin = motor_axes[int.from_bytes(axis, byteorder="big")]

    return(dir_pin, step_pin, direction, steps)


enable.value = True
while True:
    dir_pin, step_pin, direction, steps = receive_signal()
    step_motor(dir_pin, step_pin, steps, direction)
