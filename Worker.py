#! /usr/bin/env python3

import cv2
import numpy as np
import base64
import queue
from threading import *

threadNum = 0
buff1 = list()
buffLock1 = Lock()
empty1 = Semaphore(10)
full1 = Semaphore(0)
buff2 = list()
buffLock2 = Lock()
empty2 = Semaphore(10)
full2 = Semaphore(0)

class Extractor(Thread):
    def __init__(self, filename):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.filename = 'clip.mp4'
    def run(self):
        global buff1
        global buffLock1
        global empty1
        global full1
        # Initialize frame count 
        count = 0

        # open video file
        vidcap = cv2.VideoCapture(self.filename)
        
        # read first image
        success,image = vidcap.read()
        
        print(f'Reading frame {count} {success}')
        while success and count < 72:
            # get a jpg encoded frame
            success, jpgImage = cv2.imencode('.jpg', image)
        
            #encode the frame as base 64 to make debugging easier
            jpgAsText = base64.b64encode(jpgImage)

            # add the frame to the buffer
            empty1.acquire()
            buffLock1.acquire()
            buff1.append(image)
            buffLock1.release()
            full1.release()
       
            success,image = vidcap.read()
            print(f'Reading frame {count} {success}')
            count += 1
        empty1.acquire()
        buffLock1.acquire()
        buff1.append(None)
        buffLock1.release()
        full1.release()
        print('Frame extraction complete')

class Grayscale(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        global buff1
        global buffLock1
        global empty1
        global full1
        global buff2
        global buffLock2
        global empty2
        global full2
        # initialize frame count
        count = 0

        # go through each frame in the buffer until the buffer is empty
        while True:
            # get the next frame
            full1.acquire()
            buffLock1.acquire()
            frame = buff1.pop(0)
            buffLock1.release()
            empty1.release()
            if(frame is None):
                empty2.acquire()
                buffLock2.acquire()
                buff2.append(None)
                buffLock2.release()
                full2.release()
                break
            grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            empty2.acquire()
            buffLock2.acquire()
            buff2.append(grayscaleFrame)
            buffLock2.release()
            full2.release()

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame

            count += 1

        
class Display(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        global buff2
        global buffLock2
        global empty2
        global full2
        # initialize frame count
        count = 0

        # go through each frame in the buffer until the buffer is empty
        while True:
            # get the next frame
            full2.acquire()
            buffLock2.acquire()
            frame = buff2.pop(0)
            buffLock2.release()
            empty2.release()
            if(frame is None):
                break

            print(f'Displaying frame {count}')        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            count += 1

        print('Finished displaying all frames')
        # cleanup the windows
        cv2.destroyAllWindows()

Extractor('clip.mp4').start()
Grayscale().start()
Display().start()
