# Dumbbell-Microscope
Software for controlling the Team Dumbbell microscopy widget. The Dummbell microscopy widget is a set of mechanical actuators which attach to a light microscope and repeatedly image portions of an inserted slide.
The widget automatically moves the slide to image various portions of the sample and automatically focuses each slide exposure.

## Software Structure
![Software Architecture Diagram](https://drive.google.com/uc?export=view&id=1vWPpIpUUFqZDfkjHd6_QA2P0bTIv61rZ)

- `stepper_controller.py` is a CircuitPython program for the Raspberry Pi Pico which controls the widget's three stepper motors according to commands sent over serial from the api layer.
- `image_processing.py` is a Python module which identifies the most in-focus image in a series of multiple images of the same microscope field.
- `api.py` is an interop layer which handles communication with the Matlab Engine camera controller, stepper controller, and image processing module.
- `planner.py` is the main entrypoint for the software. It interacts with other components through the `api.py` layer to produce the final in-focus images.

## About Us
Team Dummbell is a student design team as part of the Praxis III course at the University of Toronto.

## Setup
1. Install the Lumenera Camera SDK as instructed in the below User Manual.
2. Install the packages listed in the `requirements.txt` file.
3. Install the packages for the microcontroller in the `microcontroller/requirements.txt` file.
4. Connect and flash the microcontroller with the `code.py` and `boot.py` programs.
5. Run `./planner.py` and follow the prompts.

## Further Resources
- [Lumenera Camera SDK](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads/lucam-software.html) and [User Manual](https://www.lumenera.com/media/wysiwyg/support/pdf/Teledyne_Lumenera-USB_Camera-API_Reference_Manual.pdf) 
- [Autofocusing Metrics](https://onlinelibrary.wiley.com/doi/full/10.1111/jmi.13064)
- [More Autofocusing Metrics](https://ieeexplore.ieee.org/abstract/document/1545017?casa_token=qrYe0ZHe4dwAAAAA:OtZUMRlPJtLn3xefLA-0QkEZlBXvot3dFesRmVs86TVNshtphdMnTmJcCTsEyw2GigXJTSM)
- [Reference Z Stacks](https://rdr.ucl.ac.uk/articles/dataset/High_Magnification_Z-Stacks_from_Blood_Films/13402301)
