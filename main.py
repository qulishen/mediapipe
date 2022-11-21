import threading
from random import randint

from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import *
import mediapipe as mp
import gamepage
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

app = QApplication([])
window = QMainWindow()
window.resize(800, 500)
window.move(400, 310)



class game_page:

    def __init__(self):
        global game_ui
        global game_dialog
        self.score=0
        self.video_size = QSize(741, 471)

        game_dialog= gamepage.Ui_Dialog()
        game_ui=QMainWindow()
        game_dialog.setupUi(game_ui)
        game_dialog.pushButton.clicked.connect(game_ui.close)
        game_dialog.label.setFixedSize(self.video_size)

        self.setup_camera()

        game_ui.show()
        window.close()
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())
        th = threading.Thread(target=self.display)
        th.start()
    def display(self):
        xlist = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        ylist = [0.5, 0.4, 0.3]

        x = randint(0, 6)
        y = randint(0, 2)

        with mp_holistic.Holistic(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as holistic:
            while self.cap.isOpened():
                success, image = self.cap.read()

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
                        self.score += 1
                        game_dialog.label_3.setText(str(self.score))

                cv2.circle(image, (int(xlist[x] * w), int(ylist[y] * h)), 30, (0, 0, 255), -1)
                text = "score"
                image = cv2.flip(image, 1)
                image = QImage(image, image.shape[1], image.shape[0],
                               image.strides[0], QImage.Format_RGB888)
                game_dialog.label.setPixmap(QPixmap.fromImage(image))


def newgame():
    newone=game_page()

label=QLabel("欢迎来到篮球训练场！",window)
label.setStyleSheet("font-size: 40pt;")
label.resize(770,200)
label.move(80,100)

button_start=QPushButton('Start',window)
button_start.move(300,300)
button_start.resize(200,100)
button_start.clicked.connect(newgame)


window.show()
app.exec_()