# This program is built to choose an initial point of an object (say surgical arm setup) and another point ad final location.
# Once the final point is reached (on second click), the instantaneous location of the object (mouse pointer) is shown pointing towards
# initial point to give directions to reach back

# Once, pointer reaches the initial point, a 'REACHED!' message is shown on the window

import imghdr
from pynput.mouse import Button, Controller, Listener
from pynput.keyboard import Key
import cv2
import numpy as np

#function to display the coordinates of the points clicked on image

def click_event(event, x, y, flags, params):

    global click_count, arr1
    global cache, img

    if event==cv2.EVENT_LBUTTONDOWN and click_count<2:
        cv2.circle(img, (x, y), 10, (255, 255, 255), thickness = -1)
        cv2.circle(img, (x, y), 3, (0, 0, 0), thickness = -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x)+','+str(y), (x, y), font, 1, (255, 0, 0), 2)
        cache = img.copy()
        click_count+=1
        if click_count==1:
            arr1.append((x, y))
    if event==cv2.EVENT_MOUSEMOVE and click_count==2 and (x, y)!=arr1[0]:
        img = cache.copy()
        cv2.circle(img, (x, y), 8, (0, 255, 255), thickness = -1)
        cv2.arrowedLine(img, (x, y), arr1[0], (0, 255, 255), 2)
        if click_count==2 and (x, y)==arr1[0]:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'REACHED!', (100, 100), font, 1, (0, 255, 255), 2)

img = np.zeroes([512, 512, 3], dtype=np.unit8)
cache = img.copy()
global click_count
click_count = 0
global arr1
arr1 = []
cv2.namedWindow('image')
cv2.setMouseCallback('image', click_event)

while (True):
    cv2.imshow('image', img)
    if cv2.waitKey(20) & 0xff == 27:
        break
cv2.destroyAllWindows()