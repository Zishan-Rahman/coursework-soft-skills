from tkinter import * #imports everything from the tkinter module so it can be used without calling tkinter
from tkinter import ttk #imports the ttk submodule from tkinter
from random import randint, uniform #imports the randint and uniform functions from the random module
from time import time, sleep #imports the time and sleep functions from the time module

#creates the attention class for the attention test
class AttentionApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(AttentionApp,self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.attempts = []
        self.resultlab = []
        self.total = 0.0
        self.count = int()
        self.max = 5
        self.pack()
        self.app()

    #confirms whether the window will be closed and the test exited
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #creates the actual test
    def app(self):
        self.lab1 = Label(self, text="We will now start testing your attention.")
        self.lab1.pack()

        self.countlab = Label(self, text="Attempt count: {0} of {1}".format(self.count,self.max))
        self.countlab.pack()

        self.startb = Button(self, text="Start the test", command=self.next)
        self.startb.pack()

    #starts the time interval, then changes the button's text and function when it's over
    def next(self):
        self.rando = uniform(0.5,10.5)
        sleep(self.rando)
        self.startb.configure(text="Press this button NOW", command=self.record)
        self.start = time()

    #shows the reaction time then, and, after the limit's reached, all the reaction times from all attempts, as well as the mean reaction time
    def record(self):
        self.end = time()
        self.timework = self.end - self.start
        self.printer = Label(self, text="Reaction time: {} seconds".format(self.timework))
        self.printer.pack()
        self.count += 1
        self.total += self.timework
        self.countlab.configure(text="Attempt count: {0} of {1}".format(self.count, self.max))
        self.dicto = dict([('Attempt Number',self.count),('Reaction Time',self.timework)])
        self.attempts.append(self.dicto)
        self.again()

    #packs a reset button, or finishes the test, if the limit is reached
    def again(self):
        if self.count < self.max:
            self.lab2 = Label(self, text="Click the below button to test again")
            self.lab2.pack()
            self.retry = Button(self, text="Retest",command=self.redo)
            self.retry.pack()
        elif self.count == self.max:
            self.finish()

    #resets the first button so the test can be reperformed
    def redo(self):
        self.printer.pack_forget()
        self.lab2.pack_forget()
        self.retry.pack_forget()
        self.startb.configure(text="Start the test", command=self.next)

    #creates, formats and shows the end results
    def finish(self):
        self.timeit = self.total / self.count

        Label(self,text="").pack()
        Label(self,text="Total times: {} seconds".format(self.total)).pack()
        Label(self,text="Total attempts: {}".format(self.count)).pack()
        Label(self,text="").pack()
        for i in range(len(self.attempts)):
            Label(self,text="Attempt {0}: {1} seconds".format(self.attempts[i]['Attempt Number'],self.attempts[i]['Reaction Time'])).pack()
        Label(self,text="").pack()
        Label(self,text="Average/Mean Reaction Time: {} seconds".format(self.timeit)).pack()

        for i in range(len(self.attempts)):
            self.resultlab.append("Attempt {0}: {1} seconds\n".format(self.attempts[i]['Attempt Number'],self.attempts[i]['Reaction Time']))

        self.resultlab.append("Average/Mean Reaction Time: {} seconds".format(self.timeit))

        self.finish = Button(self,text="Quit",command=self.kill)
        self.finish.pack()

    #closes the window
    def kill(self):
        self.master.destroy()

    #creates the string file that will be inserted to a text file at the end of an assessment
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#calls the attention test to be performed
def Attention():
    root = Tk()
    root.title("ATTENTION: Reaction Time Test")
    root.geometry("400x400")
    sign = AttentionApp(root)
    root.mainloop()

    info = sign.file()
    return info

#if the file itself is run from the main console
if __name__ == "__main__":
    Attention()
