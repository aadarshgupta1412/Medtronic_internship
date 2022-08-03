# Program to take webcam feed and reed switch input and processed it to obtain color composition and masking of colors

import cv2
import serial
import pyfirmata
import numpy as np
import matplotlib.pyplot as plt
import webcolors
from Threading import Thread
import time

def bounds(color_name):
    x = webcolors.name_to_rgb(color_name)
    y = [[[x[2], x[1], x[0]]]]
    color_name = np.unit8(y)
    hsv_color = cv2.cvtColor(color_name, cv2.COLOR_BGR2HSV)
    lowerLimit = [hsv_color[0][0][0] - 10, 50, 50]
    upperLimit = [hsv_color[0][0][0] + 10, 255, 255]
    return lowerLimit, upperLimit

def get_mask(hsv, l, u):
    lower_color = np.array(l)
    upper_color = np.array(u)
    mask1 = cv2.inRange(hsv, lower_color, upper_color)
    return mask1

def convert_image(frame, colors_array):
    #frame = cv2.imrad(image_path)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l, u = bounds(colors_array[0])
    init_mask = get_mask(hsv, l, u)
    for i in range(1, len(colors_array)):
        l, u = bounds(colors_array[i])
        #m = get_mask(hsv, l, u)
        lower_color = np.array(l)
        upper_color = np.array(u)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        init_mask = init_mask +mask
    final_mask = 255-init_mask
    #color_count = np.sum(final_mask == 0)
    res1 = cv2.bitwise_and(frame, frame, mask = init_mask)
    #res2 = cv2.bitwise_and(frame, frame, mask = final_mask)
    res2 = frame - res1

    count = np.sum(res2 == 0)
    total = np.sum(res2 != 0)
    p = 100*count/(total+count)
    return res1, res2, p

def composition(frame):

    colors = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']
    percentage = []
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for i in colors:
        l, u = bounds(i)
        lower_color = np.array(l)
        upper_color = np.array(u)
        init_mask = cv2.inRange(hsv, lower_color, upper_color)
        final_mask = 255- init_mask
        res2 = cv2.bitwise_and(frame, frame,mask = final_mask)
        imS2 = cv2.resize(res2, (640, 320))
        count = np.sum(imS2 == 0)
        total = np.sum(imS2 != 0)
        p = 100*count/(total+count)
        p = "{:.2f}".format(p)
        p = float(p)
        percentage.append(p)
    return percentage

class WebcamStream:
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id # default is 0 for main camera
        
        #opening video camera capture
        self.vcap = cv2.VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))
        print("FPS of input stream: {}").format(fps_input_stream)

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print("[Exiting] No more frames to read")
            exit(0)
        #self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.t = Thread(target = self.update, args=())
        self.t.daemon = True # daemon threads run in background
    
    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print("[Exiting] No more frames to read")
                self.stopped = True
                break
        self.vcap.release()
    
    #method to return latest read frame
    def read(self):
        return self.frame
    
    # method to stop reading frames
    def stop(self):
        self.stopped = True


webcam_stream = WebcamStream(stream_id=0) # 0 id for main camera, 1 for external webcam
webcam_stream.start()
# processing frames in input stream
num_frames_processed = 0
start = time.time()

ser = serial.Serial('COM5', 9600, timeout = 0.1) # write your port number here, for example: COM4, COM5
#board = pyfirmata.Arduino('YOUR_PORT_HERE)

#txt1 = input('Enter your color array to be removed: ')
#input1 = int(txt1)
#colors_array = txt1.split(',')
colors_array = ['burlywood']

while True:
    if webcam_stream.stopped is True:
        break
    else:
        frame = webcam_stream.read()
    # print(ser.readline())
    delay = 0.02
    time.sleep(delay)
    num_frames_processed += 1

    if (ser.readline()==b'0\n'):
        im1, im2, p = convert_image(frame, colors_array)
        #cv2.imshow('frame', frame)
        cv2.imshow('removed', im1)
        cv2.imshow('output', im2)
    
    else:
        #im1, im2, p = convert_image(frame, colors_array)
        cv2.imshow('output', frame)
        cv2.imshow('removed', im1)
        cv2.imshow('retained', im2)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

end = time.time()
webcam_stream.stop()

elapsed = end-start
fps = num_frames_processed/elapsed
print("FPS: {}, Elapsed Time: {}".format(fps, elapsed))
cv2.destroyAllWindows()
