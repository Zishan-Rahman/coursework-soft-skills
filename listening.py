#imports several modules, submodules and functions
from tkinter import *
from tkinter import messagebox
from time import sleep
from pygame import mixer
from random import randint
from ast import literal_eval

#creates the listening test class
class ListenApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(ListenApp,self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        mixer.init() #initiates the mixer submodule from pygame
        self.pack()
        self.tries = []
        self.used = []
        self.resultlab = []
        self.play = True
        self.max = 3
        self.attempts = 0
        self.correct = False
        self.right = 0
        self.creation()

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #creates the actual window and widgets for the listening test
    def creation(self): 
        self.lab1 = Label(self, text="Play the recording, then discern the text being said.")
        self.lab1.pack()

        self.lab2 = Label(self, text="Attempt count: {0} of {1}".format(self.attempts,self.max))
        self.lab2.pack()

        self.bot1 = Button(self, text="Play Now", command=self.playaudio)
        self.bot1.pack()

        self.widge = Entry(self, width=40)
        self.widge.pack()

        self.bot2 = Button(self, text="Enter", command=self.correction)
        self.bot2.pack()

        self.lab3 = Label(self, text="")
        self.lab3.pack()

    #chooses which audio files to be played
    def playaudio(self):
        if self.play and self.attempts < self.max:
            self.lab3.configure(text="")
            self.pick = randint(1,22)
            if self.pick not in self.used:
                self.used.append(self.pick)
            else:
                self.playaudio()
            self.play = False
        self.audio = str(self.pick)+".ogg"
        mixer.music.load(self.audio)
        mixer.music.play()

    #checks to see if the response is correct, and then,  if all the attempts are exhausted, the end results are compiled
    def correction(self):
        if self.attempts < self.max:
            self.attempts += 1
            self.play = True
            self.check = self.widge.get().lower().strip()
            self.dicto = dict([('audio',self.pick),('text',self.check)])
            self.tries.append(self.dicto)
            with open("Audios.txt",mode='r') as reader:
                for line in reader:
                    if str(line) == str(self.dicto)+"\n":
                        self.correct = True
            self.lab2.configure(text="Attempt count: {0} of {1}".format(self.attempts,self.max))
            if self.correct:
                self.lab3.configure(text="That is correct.")
                self.right += 1
            else:
                self.lab3.configure(text="That is incorrect.")
            self.widge.delete(0, 'end')
            self.correct = False
        if self.attempts == self.max:
            self.end()

    #compiles the end results into a list of strings
    def end(self):
        Label(self,text="").pack()
        Label(self,text="Total correct attempts: {0} of {1}".format(self.right,self.attempts)).pack()
        Label(self,text="").pack()
        self.iter = 0

        for info in self.tries:
            with open("Audios.txt",mode='r') as reader:
                for line in reader:
                    store = literal_eval(line)
                    if store["audio"] == info["audio"]:
                        self.iter += 1
                        if store["text"] == info["text"]:
                            axe = "Your response was correct"
                        else:
                            axe = "Your response was incorrect"
                        self.resultlab.append("Attempt {0}\nYour Answer: {1}\nThe Correct Answer: {2}\n{3}\n".format(self.iter, info["text"], store["text"],axe))
                        Label(self,text=self.resultlab[self.iter-1]).pack()

        self.finish = Button(self,text="Quit",command=self.kill)
        self.finish.pack()

    #ends the program
    def kill(self):
        self.master.destroy()

    #takes the data in resultlab and formats them into one string
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#loads the Listening test function (NO WEBCAM)
def Listen():
    root = Tk()
    root.title("Listening Test (NO WEBCAM)")
    root.geometry("500x500")
    listen = ListenApp(root)
    root.mainloop()
    
    box = listen.file()
    return box

#if the file itself is run from the main console
if __name__ == "__main__":
    Listen()
