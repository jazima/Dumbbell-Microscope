from typing import Tuple, Sequence, List

import numpy as np
import cv2

# Type hint for opencv image
OpenCVImage = np.ndarray

# Assignment for motor_ids 
motor_axes = {
    "x": 0,
    "y": 1,
    "focus_fine": 2,
    "focus_coarse": 3
}

###############################################################################
#                           Camera Controller API                             #
###############################################################################
def camera_controller_init() -> None:
    "Initialize the camera controller program and NamedPipe connection."
    raise NotImplementedError()

def take_image() -> OpenCVImage:
    raise NotImplementedError()

###############################################################################
#                          Stepper Controller API                             #
###############################################################################

def stepper_controller_init() -> None:
    "Initializes the serial connection to the stepper controller."
    raise NotImplementedError()

# Distance in mm per degree of rotation for the x and y axes.
x_dist_factor = float("NaN")
y_dist_factor = float("NaN")

# Size of a step in degrees.
step_degrees = 0.8

def _calculate_error(degrees: float) -> float:
    "Calculate rel error when degrees is rounded to nearest step_size_degrees."
    return abs(
        (round(degrees / step_degrees) * step_degrees - degrees) / degrees
    )

def move_x_axis(distance_mm: float, err_tol: float = 0.01) -> None:
    """Move the x axis by a specified distance in mm.

    :param distance_mm: the distance to move the axis in mm.
    :param err_tol: the maximum relative error between the commanded movement.
    and the movement rounded to the nearest step size.
    :returns: None
    :raises ValueError: when the relative error is greater than err_tol.
    """

    degrees = distance_mm / x_dist_factor
    if _calculate_error(degrees) > err_tol:
        raise ValueError(
            "Error in commanded step too high. Commanded step was"
            f"{degrees}, relative error was {_calculate_error(degrees)}."
        )

    _send_motor_control_packet(motor_axes["x"], degrees)

def move_y_axis(distance_mm: float, err_tol: float = 0.01) -> None:
    """Move the y axis by a specified distance in mm.

    :param distance_mm: the distance to move the axis in mm.
    :param err_tol: the maximum relative error between the commanded movement.
    and the movement rounded to the nearest step size.
    :returns: None
    :raises ValueError: when the relative error is greater than err_tol.
    """

    degrees = distance_mm / y_dist_factor
    if _calculate_error(degrees) > err_tol:
        raise ValueError(
            "Error in commanded step too high. Commanded step was"
            f"{degrees}, relative error was {_calculate_error(degrees)}."
        )

    _send_motor_control_packet(motor_axes["y"], degrees)

def move_fine_focus(degrees: float, err_tol: float = 0.01) -> None:
    """Move the fine focus knob by a specified distance in degrees.

    :param distance_mm: the distance to move the fine focus in degrees.
    :param err_tol: the maximum relative error between the commanded movement.
    and the movement rounded to the nearest step size.
    :returns: None
    :raises ValueError: when the relative error is greater than err_tol.
    """

    if _calculate_error(degrees) > err_tol:
        raise ValueError(
            "Error in commanded step too high. Commanded step was"
            f"{degrees}, relative error was {_calculate_error(degrees)}."
        )

    _send_motor_control_packet(motor_axes["focus_fine", degrees])

def move_coarse_focus(degrees: float, err_tol: float = 0.01) -> None:
    """Move the coarse focus knob by a specified distance in degrees.

    :param distance_mm: the distance to move the coarse focus in degrees.
    :param err_tol: the maximum relative error between the commanded movement.
    and the movement rounded to the nearest step size.
    :returns: None
    :raises ValueError: when the relative error is greater than err_tol
    """
    
    if _calculate_error(degrees) > err_tol:
        raise ValueError(
            "Error in commanded step too high. Commanded step was"
            f"{degrees}, relative error was {_calculate_error(degrees)}."
        )

    _send_motor_control_packet(motor_axes["focus_coarse"], degrees)

def _send_motor_control_packet(motor_axis: int, degrees: float) -> None:
    """Send a motor control packet.
    
    :param motor_axis: the index of the motor the packet is commanding.
    :param degrees: the number of degrees to move that axis.
    :returns: None

    An internal implementation function which directly sends motor control
    packets to the stepper controller. This does not do error checking or
    axis translation and should only be used to implement the above API functions.
    """
    raise NotImplementedError()

###############################################################################
#                            Computer Vision API                              #
###############################################################################

def analyze_z_stack(images: Sequence[OpenCVImage]) -> Tuple[List[float], int]:
    """Analyze a stack of images at varying level of focus to determine most in focus image.
    
    :param images: A sequence of images of the same microscope field taken at varying levels of focus.
    :returns: A list of floats representing the focus metric for each image and an integer
    representing the index of the most in-focus image in the stack. The focus metric is a normalized
    float [0,1] where a higher value represents a better focused image.
    """
    raise NotImplementedError()
