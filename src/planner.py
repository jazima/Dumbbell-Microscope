'''
    Planning module for Team Dumbbell malaria microscopy widget.
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

import sys
from pathlib import Path
from typing import Sequence, List, Tuple
from time import sleep

import cv2

import api

def _ack(prompt: str):
    """Prompt the user with a y/n confirmation notice given by string."""

    # strings representing either yes or no that a user may type.
    yes = ["y", "Y", "yes", "Yes", "YES"]
    no = ["n", "N", "no", "No", "NO"]

    # Get user input with the given prompt
    ack = input(prompt)

    # If the user gave input that didn't make sense, retry the prompt.
    while ack not in yes and ack not in no:
        print("You did not press y or n.")
        ack = input(prompt)

    # Exit the program if they entered no.
    if ack in no:
        sys.exit(1)

def _user_setup():
    """Interact with the user to set up the microscope for imaging."""

    print("To answer the following prompts, press y to continue or n to end the program.")
    print("Please confirm that:")
    _ack("(1) The slide is firmly positioned in the slide holder.")
    _ack("(2) The slide is currently positioned on the top left corner of the sample being imaged.")
    _ack("(3) The microscope is focused well on the current field.")
    _ack("(4) The camera is powered on and connected to the computer via USB.")
    _ack("(5) The widget is powered on and connected to the computer via USB.")
    print("Setup Complete\n\n")

def _create_out_dir(output_dir: str) -> Path:
    """Creates an output directory for images.
    :param output_dir: a string representing the output directory for images.
    :returns Path: the created output directory.

    If the output directory already exists, append an increasing index to the pathname until the directory doesn't exist.
    """
    raise NotImplementedError()

def _take_z_stack(n_z_stack: int, z_step_size: float, movement_sleep: float = 0.01) -> List[api.OpenCVImage]:
    """Take a z-stack of images. Assumes the microscope is initially in the best guess for focus. 

    :param n_z_stack: how many images in a z-stack to take per field.
    :param z_step_size: the number of degrees to turn the fine focus knob per z-step.
    :param movement_sleep: how long to wait after moving to take an image in seconds.
    """
    images = []

    # Move to the top of the z-stack
    api.move_fine_focus(z_step_size * (n_z_stack - 1) / 2.0)

    # Wait extra long because it is a long movement
    sleep(movement_sleep * 3)
    
    # Take image at the top
    images.append(api.take_image())

    # Step down one step size and take image.
    for i in range(n_z_stack - 1):
        api.move_fine_focus(-z_step_size)
        sleep(movement_sleep)
        images.append(api.take_image())

    # Move back to initial position.
    api.move_fine_focus(z_step_size * (n_z_stack - 1) / 2.0)
    return images

def main(
    x_travel_mm: float, 
    y_travel_mm: float, 
    n_fields_x: int, 
    n_fields_y: int, 
    n_z_stack: int, 
    z_step_size: float,
    output_dir: str
    ):
    """The main control loop for the widget.

    :param x_travel_mm: the distance to travel in the x direction on the sample.
    :param y_travel_mm: the distance to travel in the y direction on the sample.
    :param n_fields_x: the number of fields to take in the x direction.
    :param n_fields_y: the number of fields to take in the y direction.
    :param n_z_stack: how many images in a z-stack to take per field.
    :param z_step_size: the number of degrees to turn the fine focus knob per z-step.
    """

    _user_setup()

    print("Initializing camera module...")
    api.camera_controller_init()
    print("Camera module initialized successfully!\n")

    print("Initializing stepper controller...")
    api.stepper_controller_init()
    print("Stepper controller initialized successfully!\n")

    # Create the output directory for images after everything has successfully initialized.
    # Sets output_dir in case the directory already existed so _create_out_dir changed the name.
    output_dir = _create_out_dir(output_dir)

    print("Beginning imaging.")

    x_step_mm = x_travel_mm / n_fields_x
    y_step_mm = y_travel_mm / n_fields_y

    y_direction = 1
    for i in range(n_fields_x):
        for j in range(n_fields_y):
            images = _take_z_stack(n_z_stack, z_step_size)
            _, best_focused = api.analyze_z_stack(images)

            # Move the microscope to the best focused position
            api.move_fine_focus(z_step_size * (n_z_stack - 1 - best_focused) / 2.0)
            cv2.imwrite(str(output_dir / f"field_{i}_{j}.png"), images[best_focused])

            # Step one position
            api.move_y_axis(y_step_mm * y_direction)

        # Change directions in y.
        y_direction *= -1
        
        # Step over one position
        api.move_x_axis(x_step_mm)

    # Return to home position.
    api.move_x_axis(-x_travel_mm)

    print(f"Imaging complete. Files written to {output_dir}.")

if __name__ == "__main__":
    main(
        x_travel_mm = 20,
        y_travel_mm = 10,
        n_fields_x = 30,
        n_fields_y = 5,
        n_z_stack = 7,
        z_step_size = 20,
        output_dir="out"
    )
