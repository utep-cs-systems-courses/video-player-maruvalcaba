#! /usr/bin/env python3
# Manuel Ruvalcaba
# April 18, 2021
# Theory of Operating Systems
# Dr. Freudenthal
# Video Player: This program extracts frames from a file, converts them to grayscale, and displays them on the screen, using Producer/Consumer threads and counting semaphores.

import myVideoHelper
from threading import *

threadNum = 0

class Extractor(Thread):
    def __init__(self, filename):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.filename = filename
    def run(self):
        myVideoHelper.extractFrames(self.filename)

class Grayscale(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        myVideoHelper.convertFrames()
        
class Display(Thread):
    def __init__(self):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
    def run(self):
        myVideoHelper.displayFrames()

Extractor('clip.mp4').start()
Grayscale().start()
Display().start()
