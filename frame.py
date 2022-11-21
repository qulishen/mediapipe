import threading
import time
from random import randint

import cv2
import sys
import mediapipe as mp
from PySide2.QtCore import QTimer, QSize, Signal
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic
xlist = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
ylist = [0.5, 0.4, 0.3]

x = randint(0, 6)
y = randint(0, 2)


def video_frame():
    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            success, image = cap.read()

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            h, w, c = image.shape

            # 画图
            image.flags.writeable = True

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style())

            if results.pose_landmarks:
                rhand_x = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].x * w)
                rhand_y = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_INDEX].y * w)
                lhand_x = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].x * w)
                lhand_y = int(results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_INDEX].y * w)
                rfang = (rhand_x - xlist[x] * w) * (rhand_x - xlist[x] * w) + (rhand_y - ylist[y] * h) * (
                        rhand_y - ylist[y] * h)
                lfang = (lhand_x - xlist[x] * w) * (lhand_x - xlist[x] * w) + (lhand_y - ylist[y] * h) * (
                        lhand_y - ylist[y] * h)
                if rfang < 900 or lfang < 900:
                    x = randint(0, 6)
                    y = randint(0, 2)
                    cv2.circle(image, (int(xlist[x] * w), int(ylist[y] * h)), 30, (0, 0, 255), -1)
            cv2.circle(image, (int(xlist[x] * w), int(ylist[y] * h)), 30, (0, 0, 255), -1)
            text = "score"
            image = cv2.flip(image, 1)
