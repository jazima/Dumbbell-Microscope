# Dumbbell-Microscope
Software for controlling the Team Dumbbell microscopy widget. The Dummbell microscopy widget is a set of mechanical actuators which attach to a light microscope and repeatedly image portions of an inserted slide.
The widget automatically moves the slide to image various portions of the sample and automatically focuses each slide exposure.

## Software Structure
![Software Architecture Diagram](https://cdn.discordapp.com/attachments/934599470686019597/951632594653564988/Basic_Software_Architecture.drawio.png)

- `camera_controller.cs` is a small C# program which  with the Lumenera Infinity One microscope camera. 
    It communicates with the main application through a [NamedPipe](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes) to take and return images on command.
- `stepper_controller.py` is a CircuitPython program for the Raspberry Pi Nano or Arduino Nano Connect which controls the widget's four stepper motors according to commands sent over serial from the api layer.
- `image_processing.py` is a Python module which identifies the most in-focus image in a series of multiple images of the same microscope field.
- `api.py` is an interop layer which handles communication with the camera controller, stepper controller, and image processing module.
- `planner.py` is the main entrypoint for the software. It interacts with other components through the `api.py` layer to produce the final in-focus imaged slides.

## About Us
Team Dummbell is a student design team as part of the Praxis III course at the University of Toronto.

## Further Resources
- [Lumenera Camera SDK](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads/lucam-software.html) and [User Manual](https://www.lumenera.com/media/wysiwyg/support/pdf/Teledyne_Lumenera-USB_Camera-API_Reference_Manual.pdf) 
- [Autofocusing Metrics](https://onlinelibrary.wiley.com/doi/full/10.1111/jmi.13064)
- [More Autofocusing Metrics](https://ieeexplore.ieee.org/abstract/document/1545017?casa_token=qrYe0ZHe4dwAAAAA:OtZUMRlPJtLn3xefLA-0QkEZlBXvot3dFesRmVs86TVNshtphdMnTmJcCTsEyw2GigXJTSM)
