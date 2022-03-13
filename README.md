# Dumbbell-Microscope
Software for controlling the Team Dumbbell microscopy widget. The Dummbell microscopy widget is a set of mechanical actuators which attach to a light microscope and repeatedly image portions of an inserted slide.
The widget automatically moves the slide to image various portions of the sample and automatically focuses each slide exposure.

## Software Structure
![Software Architecture Diagram](https://doc-14-2o-docs.googleusercontent.com/docs/securesc/qik02c3jhutndbfr9ldsci0no3saq7g0/10u6641udivodu520ad0fscap10h6okn/1647211725000/15388664913180478322/15388664913180478322/14uU6BhZZhVCNyC4wY7uFhKEPqPzc2gw5?e=view&ax=ACxEAsbqGQcDbRYRX2T4dAnslUDVfWh9bOjASC46Q0Fh5-MpxsP0g4XeRKYHqoH1D7p18Vjeuitnw-cPSM2751rxJtxZbWhlzKFlldGWlBQLDFDSzjSpp475ZcyQmwHFGN3wCTE5rtJcV4JNYP2_m04r2O5CcrmuDLfRRvq5rf_yiXnQVuqD_PhFgwFyZRKyXLX1ebANGZ9JcoP9ntISLoL0Vbi6LLAHy1LcfTsLEZw8TDBLbaFv4tzkXLZSLCuIQ8HXHm9x_ugZF-gb5qGOCEg0ezcnkIa5wlNrPyoSlX84z0RbaVCaH9Smuij8_8akMCeYS8QfcJf1pqUOjPvCAUxOlfQbiXzoz_9isOtV_RzWpaVyEWDZS06GG7RiA6nQS_drvajXe0NWVLo4N_DZhj94BDUG5oCFi_dwT8CWYXIGB9oy94TQdOE_kcq8XBejFbgNnVvjQOyBImH52vQi-TlIo9yVcuuMN6vnuKsy0EQ6AwhNZRj3QqGUxEQNVIA7A83PiZnAl5h3bfP8XMsdNnK-6vq7ecDVAlBH43X0rjnb32Mv-argccf7l-8cHz7eDhlHJnScVyu2Efcjy2v2ZeNDkkUBuHGZWSb6Ef4D7WGE_Yh1jHYPmkLaYTTv3425AmZr7RvtL0ynBdctdomaU05P3WH6fmhAw-3R7_5jUkw&authuser=0&nonce=23nvc893jbnla&user=15388664913180478322&hash=9k6lg0ho9f3vb4nqkm80bkvih4fc9hjk)

- `camera_controller.cs` is a small C# program which  with the Lumenera Infinity One microscope camera. 
    It communicates with the main application through a [NamedPipe](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes) to take and return images on command.
- `stepper_controller.py` is a CircuitPython program for the Raspberry Pi Nano or Arduino Nano Connect which controls the widget's four stepper motors according to commands sent over serial from the api layer.
- `image_processing.py` is a Python module which identifies the most in-focus image in a series of multiple images of the same microscope field.
- `api.py` is an interop layer which handles communication with the camera controller, stepper controller, and image processing module.
- `planner.py` is the main entrypoint for the software. It interacts with other components through the `api.py` layer to produce the final in-focus imaged slides.

## About Us
Team Dummbell is a student design team as part of the Praxis III course at the University of Toronto.

## Setup
1. Install the Lumenera Camera SDK as instructed in the below User Manual.
2. Install the packages listed in the `requirements.txt` file.
3. Install the packages for the microcontroller in the `microcontroller_requirements.txt` file.
4. Connect and flash the microcontroller with the stepper_controller.py program.
5. Run `./planner.py` and follow the prompts.

## Further Resources
- [Lumenera Camera SDK](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads/lucam-software.html) and [User Manual](https://www.lumenera.com/media/wysiwyg/support/pdf/Teledyne_Lumenera-USB_Camera-API_Reference_Manual.pdf) 
- [Autofocusing Metrics](https://onlinelibrary.wiley.com/doi/full/10.1111/jmi.13064)
- [More Autofocusing Metrics](https://ieeexplore.ieee.org/abstract/document/1545017?casa_token=qrYe0ZHe4dwAAAAA:OtZUMRlPJtLn3xefLA-0QkEZlBXvot3dFesRmVs86TVNshtphdMnTmJcCTsEyw2GigXJTSM)
