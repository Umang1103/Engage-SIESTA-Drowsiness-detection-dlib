# Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
# face_utils for basic operations of conversion
from imutils import face_utils
# dist for calculating the euclidean distance for yawn
from scipy.spatial import distance as dist
# mixer for alarm feature
from pygame import mixer
# python user function to sent alert mail to the user
from flaskapp.users.utils import alert_mail
# utility libraries
import os
import time

# Initializing the alarm sound
mixer.init()
sound = mixer.Sound('flaskapp/alarm.wav')

# Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("flaskapp/models_dlib/shape_predictor_68_face_landmarks.dat")


def compute(a, b):
    distance = np.linalg.norm(a - b)
    return distance


def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    # Checking if it is blinked
    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0


def cal_yawn(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = dist.euclidean(top_mean, low_mean)
    return distance


class Video(object):
    def __init__(self):
        # status marking for current state
        self.sleep = 0
        self.drowsy = 0
        self.active = 0
        self.status = "! ACTIVE !"
        self.color = (0, 0, 0)
        self.outline = 2
        self.yawn_thresh = 35
        self.ptime = 0
        self.ctime = time.time()
        self.count = 0
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def close_camera(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        _, frame = self.video.read()
        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        # ---------FPS------------#
        ctime = time.time()
        self.ptime = ctime

        # detected face in faces array
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            # -------Calculating the lip distance-----#
            lip_dist = cal_yawn(landmarks)
            # print(lip_dist)
            if lip_dist > self.yawn_thresh:
                cv2.putText(frame, f'User Yawning!', (200, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 200), 2, cv2.LINE_AA)

            # The numbers are actually the landmarks which will show eye
            left_blink = blinked(landmarks[36], landmarks[37],
                                 landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43],
                                  landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            # Now judge what to do for the eye blinks
            if left_blink == 0 or right_blink == 0:
                self.count += 1
                self.sleep += 1
                self.drowsy = 0
                self.active = 0
                if self.sleep > 6:
                    self.status = "!! SLEEPING !!"
                    self.color = (0, 0, 255)

                    # If the count exceeds 25 within 60 sec, then the system hibernates
                    if self.count >= 50 and time.time()-self.ctime <= 60:
                        time.sleep(5)
                        return os.system("shutdown /h")


                    # person is feeling sleepy so we beep the alarm
                    try:
                        sound.play()
                    except:
                        # isplaying = False
                        pass
                    if self.outline < 16:
                        self.outline = self.outline + 2
                    else:
                        self.outline = self.outline - 2
                        if self.outline < 2:
                            self.outline = 2
                    cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), self.outline)

            elif left_blink == 1 or right_blink == 1 or lip_dist > self.yawn_thresh:
                self.count += 1
                self.sleep = 0
                self.active = 0
                self.drowsy += 1
                if self.drowsy > 6:
                    self.status = "! DROWSY !"
                    self.color = (106, 0, 0)
                    if self.count >= 25:
                        return alert_mail()

            else:
                self.count -= 1
                self.drowsy = 0
                self.sleep = 0
                self.active += 1
                if self.active > 6:
                    self.status = "! ACTIVE !"
                    self.color = (0, 255, 0)

            cv2.putText(frame, self.status, (220, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.color, 3)

            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

        _, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()
