from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings

i = 0


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # This function is used in views

    def get_frame(self):
        global i
        i += 1
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        cv2.imwrite('pancard/templates/pancard/imgs'+str(i)+'.jpg', image)
        return jpeg.tobytes()
