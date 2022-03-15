from time import sleep

import api

if __name__ == '__main__':
    api.move_x_axis(5)
    api.move_y_axis(3)
    api.move_fine_focus(180)

    api.move_x_axis(-5)
    api.move_y_axis(-3)
    api.move_fine_focus(-180)
