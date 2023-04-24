import notify2
import sys
import os
import math
import asyncio

import cv2
import mediapipe as mp


directory = '.'
if len(sys.argv) > 1:
    directory = sys.argv[1]

def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped

@fire_and_forget
def make_commit():
    os.system('git add ' + directory)
    os.system('git commit -m "Changes in ' + directory + ' pushed by gcommit"')
    os.system('git push')
    print('gcommit: done commit and push of ' + directory)

    notify2.init('gcommit')
    n = notify2.Notification('GCommit', 'Changes in ' + directory + ' have been pushed')
    n.show()


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands    
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

img_stretch = cv2.imread('resized.png')
rows, cols, channels = img_stretch.shape
img2gray = cv2.cvtColor(img_stretch, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
# Take only region of logo from logo image.
img_stretch_fg = cv2.bitwise_and(img_stretch, img_stretch, mask = mask_inv)

first_enter = True

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (255, 0, 0)
thickness = 2

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    h, w, c = image.shape
    desired_h = h // 2
    desired_w = 0.2 * w

    cv2.rectangle(image, (3, 3), (int(desired_w), int(desired_h)), (34, 123, 249), 3) 

    roi = image[0:rows, -1-cols:-1]
    image_bg = cv2.bitwise_and(roi, roi, mask = mask)
    dst = cv2.add(image_bg, img_stretch_fg)
    image[0:rows, -1-cols:-1] = dst

    # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 0:
                    pos0 = (cx, cy)
                if id == 12:
                    pos1 = (cx, cy)
                if id == 8:
                    pos_pointer = (cx, cy)

            # cv2.circle(image, pos_pointer, 10, (0, 0, 255), cv2.FILLED)

            distance=(pos0[0] - pos1[0]) * (pos0[0] - pos1[0]) + (pos0[1] - pos1[1]) * (pos0[1] - pos1[1])
            distance=math.sqrt(distance)

            if distance < 0.2 * h:
                cv2.putText(image, 'Good distance! Stretch your arm to commit.', (260, 30), font, fontScale, (135, 203, 185), thickness, cv2.LINE_AA)

                if (pos_pointer[0] < desired_w and pos_pointer[1] < desired_h):
                    cv2.putText(image, 'ok, uploaded', (30, int(h - 30)), font, fontScale, (135, 203, 185), thickness, cv2.LINE_AA)
                    if (first_enter):
                        print('pushing now')
                        make_commit()
                        print('out of pushing')
                        first_enter = False
                else:
                    first_enter = True

            else:
                cv2.putText(image, 'move back', (30, int(h - 30)), font, fontScale, (34, 123, 249), thickness, cv2.LINE_AA)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", image)
    if cv2.waitKey(1) == 27:                            # [Esc] for quitting
        break


cap.release()
cv2.destroyAllWindows()