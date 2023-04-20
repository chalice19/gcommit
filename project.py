import notify2
import sys
import os

import cv2
import mediapipe as mp


directory = '.'
if len(sys.argv) > 1:
    directory = sys.argv[1]

def make_commit():
    os.system('git add ' + directory)
    os.system('git commit -m "Changes in ' + directory + ' pushed by gcommit"')
    os.system('git push')

    notify2.init('app name')
    n = notify2.Notification('GCommit', 'Changes in ' + directory + ' have been pushed')
    n.show()


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

first_enter = True

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8 :
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    if (cy < 0.1 * h):
                        if (first_enter):
                            make_commit()
                            first_enter = False
                    else:
                        first_enter = True

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", image)
    if cv2.waitKey(1) == 27:                            # [Esc] for quitting
        break