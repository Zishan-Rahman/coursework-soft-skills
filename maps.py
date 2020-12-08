#imports several modules, submodules and functions
from tkinter import *
from tkinter import messagebox
from tkinter import _setit as tke
from PIL import Image, ImageTk
from ast import literal_eval
from random import randint

#much of the code from this class was adapted from this tutorial: https://pythonbasics.org/tkinter-image/
#the code from the tutorial has been further developed by me to include more functions within the class
#it defines the image viewer class, which displays the image depending on the randomly selected test and questions
class View(Frame):
    def __init__(self,master,into):
        Frame.__init__(self,master)
        self.master.protocol("WM_DELETE_WINDOW",self.reopen)
        self.master.iconbitmap('aclogo.ico')
        self.stringer = ""
        self.into = into
        self.contain()
        self.pack(fill=BOTH, expand=1)
        self.make()

    #reopens the image window if it is closed
    def reopen(self):
        self.master.destroy()
        root = Toplevel()
        app = View(root,self.into)
        root.wm_title("Table view")
        root.mainloop()        

    #shows the image in a window
    def make(self):
        maptable = Image.open(self.stringer)
        store = ImageTk.PhotoImage(maptable)
        amgo = Label(self,image=store)
        amgo.image = store
        amgo.place(x=0,y=0)

    #closes the window once and for all
    def kill(self):
        self.master.destroy()

    #chooses a random image to be shown
    def contain(self):
        if self.into in (1,2):
            self.stringer = "tubemap{}.png".format(self.into)
            if self.into == 1:
                self.master.geometry("472x337")
            elif self.into == 2:
                self.master.geometry("333x289")
        elif self.into in (3,4):
            self.stringer = "schedule{}.png".format(self.into)
            if self.into == 3:
                self.master.geometry("670x473")
            elif self.into == 4:
                self.master.geometry("670x473")

#defines the class that shows the actual questionnaire
class MapQuestions(Frame):
    #initiates the class's initial characteristics
    def __init__(self,master,rando):
        super(MapQuestions, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW",self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.rando = rando
        self.max = 3
        self.used = []
        self.resultlab = []
        self.questions = []
        self.select = []
        self.pack()
        if self.rando == 1:
            self.due("tubemap1.txt")
            self.resultlab.append("Picture used: Tube Map Segment 1\n")
        elif self.rando == 2:
            self.due("tubemap2.txt")
            self.resultlab.append("Picture used: Tube Map Segment 2\n")
        elif self.rando == 3:
            self.due("timetable1.txt")
            self.resultlab.append("Picture used: Student Timetable 1\n")
        elif self.rando == 4:
            self.due("timetable2.txt")
            self.resultlab.append("Picture used: Student Timetable 1\n")
        self.imgview()

    #confirms with the user whether they want to close the window and end the questionnaire early
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.resultlab.append("This test was either not attempted or not fully completed.")
            self.end()

    #shows the image window alongside the questionnaire
    def imgview(self):
        root = Toplevel()
        self.app = View(root,self.rando)
        root.wm_title("Table view")
        root.mainloop()
        
    #selects a list of questions from the relevant text file, then creates the questionnaire and displays the window
    def due(self,readone):
        with open(readone,"r") as reader:
            for line in reader:
                store = literal_eval(line)
                self.questions.append(store)

        while len(self.select) < self.max:
            sct = randint(0,len(self.questions)-1)
            txc = self.questions[sct]
            if txc not in self.used:
                self.select.append(txc)
                self.used.append(txc)

        self.indy = 0

        Label(self,text="Answer the three questions given to you based on the tube map or timetable given to you.").pack()
        if self.rando in (1, 2):
            Label(self,text="Brown: Bakerloo\nPink: Circle\nYellow: Hammersmith and City\nGreen: District\nRed: Central\nDouble Blue Lines: TfL Rail\nDouble Orange Lines: Overground").pack()
        elif self.rando in (3, 4):
            Label(self,text="Period 1: 8:30PM-9:30PM\nPeriod 2: 9:30AM-10:30AM\nPeriod 3: 10:50AM-11:50AM\nPeriod 4: 11:50AM-12:50PM\nPeriod 5: 2:00PM-3:00PM (certain questions only)\nBreak: 10:30AM-10:50AM\nLunch: 1:10PM-2:00PM (certain questions only)").pack()
        self.quest = Label(self,text=self.select[self.indy]['question'])
        self.quest.pack()
        self.counter = Label(self,text="Question {0} of {1}".format(self.indy+1,self.max))
        self.counter.pack()

        self.listdo = (self.select[self.indy]['ans1'], self.select[self.indy]['ans2'], self.select[self.indy]['ans3'], self.select[self.indy]['ans4'])
        self.bods = StringVar(self)
        self.bods.set("Select an answer")
        self.choices = OptionMenu(self,self.bods,*self.listdo)
        self.choices.pack()
        self.bot1 = Button(self,text="Enter Choice",command=lambda: self.checkandpass(readone))
        self.bot1.pack()
        self.lab1 = Label(self,text="")
        self.lab1.pack()

    #checks if the response selected was correct, and appends the question, response and result to resultlab to be formatted at the end
    def checkandpass(self,filename):
        if self.indy < self.max:
            if self.bods.get() == self.select[self.indy]['correct']:
                self.correct = True
            else:
                self.correct = False

            if self.correct:
                self.endstring = "Your response was correct"
            else:
                self.endstring = "Your response was incorrect"

            self.resultlab.append("Question {0}: {1}\nYour response: {2}\nCorrect Response: {3}\n{4}\n".format(self.indy+1,self.select[self.indy]['question'],self.bods.get(),self.select[self.indy]['correct'],self.endstring))
            self.indy += 1
            
            try:
                self.listdo = (self.select[self.indy]['ans1'], self.select[self.indy]['ans2'], self.select[self.indy]['ans3'], self.select[self.indy]['ans4'])
                self.bods.set("Select an answer")
                self.choices['menu'].delete(0, 'end')
                for i in self.listdo:
                    self.choices['menu'].add_command(label=i,command=tke(self.bods,i))
                    self.bods.set("Select an answer")
                self.quest.configure(text=self.select[self.indy]['question'])
                self.counter.configure(text="Question {0} of {1}".format(self.indy+1,self.max))
            except:
                self.x = self.file()
                self.lab1.configure(text="\n"+self.x)
                self.endit = Button(self,text="Quit",command=self.end)
                self.endit.pack()

    #kills the application (both windows)
    def end(self):
        try:
            self.app.kill()
            self.master.destroy()
        except:
            self.master.destroy()

    #formats the strings in resultlab into one large string to be returned (and put into a text file later in a full assessment)
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#defines the functions that loads the maps and timetables test, randomly selecting a map or timetable to be used for the test
def ReadMap():
    randnum = randint(1,4)
    root = Tk()
    root.title("Maps + Timetables Test")
    root.geometry("700x500")
    app = MapQuestions(root, randnum)
    root.mainloop()

    box = app.file()
    return box

#if the file itself is run from the main console
if __name__ == "__main__":
    print(ReadMap())
