from time import sleep

import cv2

import api

if __name__ == '__main__':
    api.camera_controller_init()

    cv2.imshow(
        api.take_image()
    )
    
    sleep(20)
