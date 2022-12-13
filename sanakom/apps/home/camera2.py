import cv2, io, base64
from PIL import Image
import threading
from time import sleep
import numpy as np
from apps.home.GazeTracking.gaze_tracking import GazeTracking
import csv
import matplotlib as plt
import seaborn as sns
trainedfacedata = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gaze = GazeTracking()
eye_1x_positions = list()
eye_1y_positions = list()
eye_2x_positions = list()
eye_2y_positions = list()

class VideoCamera(object):
    def __init__(self):

        self.to_process = []
        self.output_image_rgb = []
        self.output_image_bgr = []
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return
        input_str = self.to_process.pop(0)
        imgdata = base64.b64decode(input_str)
        input_img = np.array(Image.open(io.BytesIO(imgdata)))
        """ h
        After getting the image you can do any preprocessing here
        """
        # ______________________________________Performing some pre processing______________________________________________

        bgr_image = cv2.flip(input_img, 1)  # Flip the image

        # img = cv2.imread("me5.png")
        frame = bgr_image
        #gaze = GazeTracking()


        frame = bgr_image

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
        
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        center_pupil_point_x = gaze.pupil_center_coords_x()
        center_pupil_point_y = gaze.pupil_center_coords_y()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31),
                    1)

        with open('coordinates.csv', 'a') as newFile:
            newFileWriter = csv.writer(newFile)
            if center_pupil_point_x != None:
                newFileWriter.writerow([float(center_pupil_point_x), float(center_pupil_point_y)])
            else:
                pass
            #cv2.imshow("Demo", frame)




            # We get a new frame from the webcam



        #cv2.destroyAllWindows()
            # cv2.imshow("me5.png", frame)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)# Changing color from bgr to rgb

        # ____________________________________________________________________________________________________________________

        ret, rgb_jpeg = cv2.imencode('.jpg', rgb_image)
        _, bgr_jpeg = cv2.imencode('.jpg', rgb_image)

        self.output_image_rgb.append(rgb_jpeg.tobytes())
        self.output_image_bgr.append(bgr_jpeg.tobytes())

        #plt.scatter(eye_1x_positions, eye_1y_positions)
        #plt.show()
        #sns.set()





    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process.append(input)

    def get_frame(self):
        while not self.output_image_rgb:
            sleep(0.05)
        return self.output_image_rgb.pop(0), self.output_image_bgr.pop(0)
    def data(self):
        data = list(zip(eye_1x_positions, eye_1y_positions))
        return data




"""
# def stringToImage(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     return np.array(Image.open(io.BytesIO(imgdata)))
"""