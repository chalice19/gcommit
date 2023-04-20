import notify2
import sys
import os

import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 0, 0)
thickness = 2

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
                if id==0:
                    pos0=(cx,cy)
                if id==12:
                    pos1=(cx, cy)
                if id == 20 :
                    distance=(pos0[0]-pos1[0])*(pos0[0]-pos1[0])+(pos0[1]-pos1[1])*(pos0[1]-pos1[1])
                    distance=math.sqrt(distance)
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    cv2.putText(image, str(f'{distance:.0f}'), (cx, cy), font, fontScale, color, thickness, cv2.LINE_AA)
                    if distance<0.2*h:
                        cv2.putText(image, 'good distance', (cx, cy-10), font, fontScale, (0,255,0), thickness, cv2.LINE_AA)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", image)
    cv2.waitKey(1)

# directory = '.'
# if len(sys.argv) > 1:
#     directory = sys.argv[1]

# os.system('git add ' + directory)
# os.system('git commit -m "Changes in ' + directory + ' pushed by gcommit"')
# os.system('git push')

# notify2.init('app name')
# n = notify2.Notification('GCommit', 'Changes in ' + directory + ' have been pushed')
# n.show()