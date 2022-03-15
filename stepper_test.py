from time import sleep

import api

if __name__ == '__main__':
    api.stepper_controller_init()

    sleep(0.05)

    api.move_x_axis(5)
    api.move_y_axis(3)
    api.move_fine_focus(180)

    sleep(0.05)
    
    api.move_x_axis(-5)
    api.move_y_axis(-3)
    api.move_fine_focus(-180)
