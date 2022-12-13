import cv2, io, base64
from PIL import Image
import threading
from time import sleep
import numpy as np
from apps.home.GazeTracking.gaze_tracking import GazeTracking
from fer import FER
import time
from apps.home.Emotionrec import autism_detector,aut_percentage,firstphase,secondphase
score1 = 0
score2 = 0

trainedfacedata = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detection = FER()


class VideoCamera4(object):
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
        endtime = time.time() + 10
        while time.time() < endtime:
            input_str = self.to_process.pop(0)
            imgdata = base64.b64decode(input_str)
            input_img = np.array(Image.open(io.BytesIO(imgdata)))
            """ h
            After getting the image you can do any preprocessing here
            """
            # ______________________________________Performing some pre processing______________________________________________

            bgr_image = cv2.flip(input_img, 1)  # Flip the image

            left = 400
            top = 500
            right = 3800
            bottom = 4000

            cropped = bgr_image
            # cv2.imshow("img", cropped)
            # Converting image to grayscale
            # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite('cropped_grayscale.jpg', gray)

            # Detecting emotions of the human with FER module and printing the output
            # image_path = cv2.imread('cropped_grayscale.jpg')
            all_emotions = detection.detect_emotions(cropped)
            all_emotion_list = list(all_emotions)
            print(f'***This is the complete list of all emotions in the human:{all_emotion_list}')

            # image_path = cv2.imread('cropped_grayscale.jpg')
            # detection = FER()
            top_emotion = detection.top_emotion(cropped)
            top_emotion_list = list(top_emotion)
            print(f'***This is the dominant emotion in the human: {top_emotion_list}')

            # Converting FER output into list
            converting_to_list = list(top_emotion)
            mood, per = converting_to_list

            # appending the detected mood and its percent dominance into two new lists.
            emotion_detected = [mood]
            per_detected = [per]
            global score1
            sp,score1=firstphase(emotion_detected)
            print(
                f'{sp}, with {aut_percentage(per_detected)}% of the odd emotion, which shows'
                f' a lack of interest.')

            # We get a new frame from the webcam

            # cv2.destroyAllWindows()
            # cv2.imshow("me5.png", frame)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # Changing color from bgr to rgb

            # ____________________________________________________________________________________________________________________

            ret, rgb_jpeg = cv2.imencode('.jpg', rgb_image)
            _, bgr_jpeg = cv2.imencode('.jpg', rgb_image)

            self.output_image_rgb.append(rgb_jpeg.tobytes())
            self.output_image_bgr.append(bgr_jpeg.tobytes())
        endtime = time.time() + 10
        while time.time() < endtime:
            input_str = self.to_process.pop(0)
            imgdata = base64.b64decode(input_str)
            input_img = np.array(Image.open(io.BytesIO(imgdata)))
            """ h
            After getting the image you can do any preprocessing here
            """
            # ______________________________________Performing some pre processing______________________________________________

            bgr_image = cv2.flip(input_img, 1)  # Flip the image

            left = 400
            top = 500
            right = 3800
            bottom = 4000

            cropped = bgr_image
            # cv2.imshow("img", cropped)
            # Converting image to grayscale
            # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite('cropped_grayscale.jpg', gray)

            # Detecting emotions of the human with FER module and printing the output
            # image_path = cv2.imread('cropped_grayscale.jpg')
            all_emotions = detection.detect_emotions(cropped)
            all_emotion_list = list(all_emotions)
            print(f'***This is the complete list of all emotions in the human:{all_emotion_list}')

            # image_path = cv2.imread('cropped_grayscale.jpg')
            # detection = FER()
            top_emotion = detection.top_emotion(cropped)
            top_emotion_list = list(top_emotion)
            print(f'***This is the dominant emotion in the human: {top_emotion_list}')

            # Converting FER output into list
            converting_to_list = list(top_emotion)
            mood, per = converting_to_list

            # appending the detected mood and its percent dominance into two new lists.
            emotion_detected = [mood]
            per_detected = [per]
            global score2
            sp, score2 = secondphase(emotion_detected)
            print(
                f'{sp}, with {aut_percentage(per_detected)}% of the odd emotion, which shows'
                f' a lack of interest.')

            # We get a new frame from the webcam

            # cv2.destroyAllWindows()
            # cv2.imshow("me5.png", frame)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)  # Changing color from bgr to rgb

            # ____________________________________________________________________________________________________________________

            ret, rgb_jpeg = cv2.imencode('.jpg', rgb_image)
            _, bgr_jpeg = cv2.imencode('.jpg', rgb_image)

            self.output_image_rgb.append(rgb_jpeg.tobytes())
            self.output_image_bgr.append(bgr_jpeg.tobytes())



        #plt.scatter(eye_1x_positions, eye_1y_positions)
        #plt.show()
        #sns.set()



    def score(self):
        self.totalscore = score1+score2
        return self.totalscore

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





"""
# def stringToImage(base64_string):
#     imgdata = base64.b64decode(base64_string)
#     return np.array(Image.open(io.BytesIO(imgdata)))
"""