#imports and initiates several modules
import cv2 as cv
import numpy as np
from pygame import mixer
mixer.init()
from random import randint
from tkinter import *
from tkinter import messagebox
import time

#the class for the whole webcam test, which initiates the webcam test
class ViewCam:
    #initiates the class's initial properties
    def __init__(self):
        self.intro()
        self.used = []
        self.resultlab = []
        self.construct = False
        self.assembleaudio()
        #MUCH OF THE BELOW CODE WAS TAKEN FROM OR INFLUENCED BY A YOUTUBE TUTORIAL AND ADAPTED INTO AN OBJECT-ORIENTED FORMAT
        #THIS IS THE TUTORIAL: https://www.youtube.com/watch?v=88HdqNDQsEk
        self.fc = cv.CascadeClassifier('(DO NOT MARK) haarcascade_frontalface_default.xml')
        self.ec = cv.CascadeClassifier('(DO NOT MARK) haarcascade_eye.xml')
        self.vid = cv.VideoCapture(0)
        self.perform = True
        self.play = True
        self.timerstart = 0
        self.start = time.time() - self.timerstart
        self.frames = 0
    
        while self.perform:
            self.playaudio()
            self.r,self.im = self.vid.read()
            self.gr = cv.cvtColor(self.im, cv.COLOR_BGR2GRAY)
            self.fcs = self.fc.detectMultiScale(self.gr)
            for (x,y,w,h) in self.fcs:
                self.exist1 = cv.rectangle(self.im, (x,y), (x+w,y+h), (255,0,0), 2)
                self.imr_gr = self.gr[y:y+h,x:x+w]
                self.imr = self.im[y:y+h,x:x+w]
                self.eyes = self.ec.detectMultiScale(self.imr_gr)
                for (ex,ey,ew,eh) in self.eyes:
                    self.exist2 = cv.rectangle(self.imr, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)
                    self.detection()

            cv.imshow('Listening Test for WEBCAMS',self.im)
            self.k = cv.waitKey(30) & 0xff
            if self.k == 13 or self.timerstart >= 30:
                self.resultlab.append("Time of test: {} seconds\nNumber of frames (captures of face and eyes): {}\n".format(self.timerstart,self.frames))
                self.perform = False
                break

            self.play = True
                
        self.vid.release()
        cv.destroyAllWindows()
        
    #picks a list of three audio files to be played
    def assembleaudio(self):
        while len(self.used) != 3:
            self.pick = randint(1,22)
            if self.pick not in self.used:
                self.used.append(self.pick)
            else:
                self.assembleaudio()

    #plays the audio after (a range of) 0 and/or 10 and/or 20 seconds
    def playaudio(self):
        if self.timerstart >= 0 and self.timerstart <= 0.1 and self.play:
            self.audio = str(self.used[0])+".ogg"
            mixer.music.load(self.audio)
            mixer.music.play(1)
        elif self.timerstart >= 10 and self.timerstart <= 10.1 and self.play:
            self.audio = str(self.used[1])+".ogg"
            mixer.music.load(self.audio)
            mixer.music.play(1)
        elif self.timerstart >= 20 and self.timerstart <= 20.1 and self.play:
            self.audio = str(self.used[2])+".ogg"
            mixer.music.load(self.audio)
            mixer.music.play(1)
        self.play = False

    #introduces the program to the user
    def intro(self):
        mixer.music.load("webcam_intro.ogg")
        mixer.music.play()
        temp = Tk()
        temp.overrideredirect()
        messagebox.showinfo("Test Instructions","The STUDENT has to look at the webcam as the random audio plays (or doesn't).\nThe test will end after around 30 seconds OR when the Enter button is pressed early.",icon="info")
        try:
            temp.withdraw()
            temp.destroy()
            mixer.music.stop()
        except:
            mixer.music.stop()

    #if the student's eyes are detected, it increments the number of frames
    #the more students look, the higher the number of frames
    def detection(self):
        self.timerstart = time.time() - self.start
        if self.exist1.any() == True:
            if self.exist2.any() == True:
                self.frames += 1

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#creates the main function for the webcam test
def Read():
    view = ViewCam()
    box = view.file()
    return box

#if the file itself is run from the main console
if __name__ == "__main__":
    print(Read())
