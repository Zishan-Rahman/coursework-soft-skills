#AC Soft Skills Assessment Program
#Authored by Zishan Rahman
#AQA A level Computer Science Non-Examined Assessment
#To be marked by Thursday 19th March 2020

from tkinter import * #imports the tkinter module to be used without directly calling tkinter
from tkinter import messagebox, ttk, scrolledtext #imports the messagebox and ttk sub-modules to be used without directly calling them
import subprocess #imports the subprocess module
from pygame import mixer #imports the mixer submodule from pygame
mixer.init() #initiates mixer
import sqlite3 as sql #imports sqlite3, to execute sql commands, and rename it sql to make it easier to type
import os #imports the built-in os module
import hashlib #imports the built-in hashlib module, which generates the text file names, using algorithms supported by OpenSSL
from datetime import datetime #imports the built-in datetime module

#the following are python files that store 'tests' to be performed, and the results returned in the form of a text file
#they have all been written by me and count towards the coursework mark
import questionnaires
import maps
import attention
import listening
import webcam

#creates the initial database if it isn't in the same folder as the program
if not os.path.isfile("TestSubjectData.db"):
    db = sql.connect("TestSubjectData.db")
    subprocess.check_call(["attrib","+H","TestSubjectData.db"]) #hides the database when it is created
    c = db.cursor()
    c.execute('''CREATE TABLE "Supervisor" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Forename"	text,
	"Surname"	text,
	"Username"	text,
	"Password"	text
)''')
    c.execute('''CREATE TABLE "Subject" (
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Forename"	text,
	"Surname"	text,
	"TestCount"	INTEGER
)''')
    c.execute('''CREATE TABLE "Activity" (
	"ActivityName"	TEXT NOT NULL PRIMARY KEY UNIQUE
)''')
    c.execute('''CREATE TABLE "Test" (
	"TestID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"SubjectID"	INTEGER,
	"SupervisorID"	INTEGER,
	"DateDone"	datetime,
	"Feedback"	TEXT,
	FOREIGN KEY("SubjectID") REFERENCES "Subject"("ID"),
	FOREIGN KEY("SupervisorID") REFERENCES "Supervisor"("ID")
)''')
    db.commit()
    c.execute('''INSERT INTO Activity VALUES("Social Skills")''')
    c.execute('''INSERT INTO Activity VALUES("Confidence")''')
    c.execute('''INSERT INTO Activity VALUES("Life Skills")''')
    c.execute('''INSERT INTO Activity VALUES("Listening Skills (with webcam)")''')
    c.execute('''INSERT INTO Activity VALUES("Listening Skills (without webcam)")''')
    c.execute('''INSERT INTO Activity VALUES("Reading Maps and Timetables")''')
    c.execute('''INSERT INTO Activity VALUES("Attention")''')
    c.execute('''INSERT INTO Activity VALUES("Organisation")''')
    c.execute('''INSERT INTO Activity VALUES("Motivation")''')
    c.execute('''INSERT INTO Activity VALUES("Self-Awareness")''')
    db.commit()
    db.close()

#opens the initial database if it is in the same folder as the program
if os.path.isfile("TestSubjectData.db"):
    db = sql.connect("TestSubjectData.db")
    c = db.cursor()

#creates the SelectApp GUI class, which launches the landing page.
class SelectApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master,forename,surname):
        super(SelectApp,self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.resultlab = []
        self.one = True
        self.forename = forename
        self.surname = surname
        self.pack()
        self.create()
        
    #confirms whether the program will be closed
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this? You haven't even started a test yet!"):
            try:
                self.studins.destroy()
                self.prog.destroy()
                self.master.destroy()
            except:
                try:
                    self.prog.destroy()
                    self.master.destroy()
                except:
                    try:
                        self.studins.destroy()
                        self.master.destroy()
                    except:
                        self.master.destroy()
                
    #creates the Student list
    def listmake(self,derive):
        c.execute('SELECT Forename, Surname FROM Subject')
        lis = c.fetchall()
        for i in range(0,len(lis)):
            first = lis[i][0]
            last = lis[i][1]
            namo = first + " " + last
            derive.append(namo.strip())
        db.commit()
        return derive

    #for restarting the landing page whenever a student is added to the database
    def classinitagain(self):
        root = Tk()
        root.title("AC Soft Skills Test Selection")
        root.geometry("500x500")
        sign = SelectApp(root, self.forename, self.surname)
        root.mainloop()

    #creates the initial landing page
    def create(self):

        ac = ["None Selected"]

        c.execute('''SELECT * FROM Activity''')
        act = c.fetchall()
        for i in range(len(act)):
            ac.append(act[i][0])

        name = "Hello, " + str(self.forename) + " " + str(self.surname) + "!"
        self.labname = Label(self,text=name)
        self.labname.pack()
        self.lab1 = Label(self, text="Select up to 5 options from {} tests".format(str(len(ac)-1)))
        self.lab1.pack()
        Label(self,text="").pack()
        
        self.lake = self.listmake([])
        self.laker = StringVar(self)
        self.laker.set("Select a student")

        try:
            self.studlab = Label(self,text="Please select a student from the dropdown menu below.")
            self.drop6 = OptionMenu(self,self.laker,*self.lake,command=self.tcounter)
            self.studlab.pack()
            self.drop6.pack()
            self.desclab = Label(self,text="No student selected")
            self.desclab.pack()    
        except:
            self.crlabel = Label(self, text="Go to Add New Student to put in a student's details.\nYou need to select a student before performing a test.")
            self.crlabel.pack()

        Label(self,text="").pack()

        self.dr1 = StringVar(self)
        self.dr1.set("None Selected")
        self.dr2 = StringVar(self)
        self.dr2.set("None Selected")
        self.dr3 = StringVar(self)
        self.dr3.set("None Selected")
        self.dr4 = StringVar(self)
        self.dr4.set("None Selected")
        self.dr5 = StringVar(self)
        self.dr5.set("None Selected")

        self.drop1 = OptionMenu(self,self.dr1,*ac,command=self.retext)
        self.drop2 = OptionMenu(self,self.dr2,*ac,command=self.retext)
        self.drop3 = OptionMenu(self,self.dr3,*ac,command=self.retext)
        self.drop4 = OptionMenu(self,self.dr4,*ac,command=self.retext)
        self.drop5 = OptionMenu(self,self.dr5,*ac,command=self.retext)
        
        for i in [self.drop1,self.drop2,self.drop3,self.drop4,self.drop5]:
            i.pack()

        Label(self,text="").pack()

        self.proco = Button(self, text="Start Test",command=self.confirm)
        self.proco.pack()
        self.testarch = Button(self, text="Test Archive", command=self.studlist)
        self.testarch.pack()
        self.addstud = Button(self, text="Add New Student",command=self.studinsert)
        self.addstud.pack()
        self.logout = Button(self, text="Log Out",command=self.confirmlogout)
        self.logout.pack()

    #confirms whether the student will log out
    def confirmlogout(self):
        if messagebox.askokcancel("Log Out?","Are you sure you want to sign out?"):
            self.Main()

    #creates the login window if the user confirms they want to log out
    def Main(self):
        try:
            self.studins.destroy()
            self.prog.destroy()
            self.master.destroy()
        except:
            try:
                self.prog.destroy()
                self.master.destroy()
            except:
                try:
                    self.studins.destroy()
                    self.master.destroy()
                except:
                    self.master.destroy()
                    
        root = Tk()
        root.title("Welcome to the Soft Skills Assessment Program!")
        root.geometry("400x400")
        sign = SignApp(root)
        root.mainloop()        

    #creates the batting order of the assessment, then confirms whether the test will go ahead
    def confirm(self):
        if self.laker.get() != "Select a student":
            self.used = []
            for i in (self.dr1.get(),self.dr2.get(),self.dr3.get(),self.dr4.get(),self.dr5.get()):
                if i not in self.used and i != "None Selected":
                    self.used.append(i)

            self.listn = ""
            for i in range(len(self.used)):
                self.listn += "Test {}: {}\n".format(i+1,self.used[i])
            self.listn += "\nYou are doing this for {}. Do you want to proceed?".format(self.laker.get())

            self.namestore = self.laker.get()

            if len(self.used) > 0:
                if messagebox.askokcancel("Confirm your selection",self.listn):
                    self.master.destroy()
                    self.doalltests()
            elif len(self.used) == 0:
                messagebox.showerror("No tests selected","Please select at least one test before continuing.")

        elif self.laker.get() == "Select a student":
            messagebox.showerror("No student selected","Please select a student before performing a test.\nIf a student needs to be added to the database, there is a button for doing so.")

    #gets the current date
    def assembledate(self):
        now = datetime.now()
        return now

    #gets the supervisor's name
    def namesake(self):
        return "{} {}".format(self.forename,self.surname)

    #executes each test in order, appending the results to a list
    def doalltests(self):
        self.resultlab.append("""AC Soft Skill Assessment
Student: {0}
Assessor: {1}
Date of assesment initiation: {2}\n""".format(self.namestore,self.namesake(),self.assembledate()))
        for i in range(0,len(self.used)):
            if self.used[i] == "Social Skills":
                self.x = questionnaires.Social()
            elif self.used[i] == "Confidence":
                self.x = questionnaires.Mantra()
            elif self.used[i] == "Life Skills":
                self.x = questionnaires.LifeSkills()
            elif self.used[i] == "Listening Skills (with webcam)":
                self.x = webcam.Read()
            elif self.used[i] == "Listening Skills (without webcam)":
                self.x = listening.Listen()
            elif self.used[i] == "Reading Maps and Timetables":
                self.x = maps.ReadMap()
            elif self.used[i] == "Attention":
                self.x = attention.Attention()
            elif self.used[i] == "Organisation":
                self.x = questionnaires.Organise()
            elif self.used[i] == "Motivation":
                self.x = questionnaires.Motivation()
            elif self.used[i] == "Self-Awareness":
                self.x = questionnaires.SelfAware()
            self.resultlab.append("\nTest number: {0}\nTest: {1}\n{2}\n".format(i+1,self.used[i],self.x))
        self.addnotes()
        self.u = self.file()
        self.hashit = hashlib.md5(self.u.encode())
        self.hasho = self.hashit.hexdigest()
        self.thisname = str(self.hasho)+".txt"
        self.flie = open(self.thisname, "w+")
        self.flie.write(self.u)
        subprocess.check_call(["attrib","+H",self.thisname]) #hides the text document while it's being created
        self.flie.close()
        self.sqlmake()
        self.compile_results()

    #puts the test into the database so the results can be retrieved later
    def sqlmake(self):
        c.execute('''SELECT ID FROM Subject WHERE Forename=? AND Surname=?''',(self.namestore.split(' ',1)[0],self.namestore.split(' ',1)[1],))
        self.id1 = c.fetchall()
        self.idst = self.id1[0][0]
        c.execute('''SELECT ID FROM Supervisor WHERE Forename=? AND Surname=?''',(self.forename,self.surname,))
        self.id2 = c.fetchall()
        self.idsu = self.id2[0][0]
        c.execute('''INSERT INTO Test(SubjectID,SupervisorID,DateDone,Feedback) VALUES (?,?,?,?)''',(self.idst,self.idsu,datetime.now(),self.thisname,))
        db.commit()
        c.execute('''SELECT TestCount FROM Subject WHERE ID=?''',(self.idst,))
        self.tsct = c.fetchall()
        self.testcount = self.tsct[0][0]
        self.testcount += 1
        c.execute('''UPDATE Subject SET TestCount=? WHERE ID=?''',(self.testcount,self.idst,))
        db.commit()

    #opens the additional notes window for assessors to input details
    def addnotes(self):
        goc = Tk()
        goc.title("Additional Notes for Assessors")
        goc.iconbitmap('aclogo.ico')
        cog = Text(goc)
        cog.pack()
        Button(goc, text="Finish", command=lambda: self.saveit(cog,goc)).pack()
        messagebox.showinfo("Additional Notes for Assessors", "Write any more details about the test here.",icon="info")
        goc.mainloop()

    #appends the resultlab list with the test results
    def saveit(self,cog,goc):
        tot = cog.get("1.0","end-1c")
        self.resultlab.append("\nAdditional Notes:\n{}\n".format(tot))
        cog.pack_forget()
        goc.destroy()

    #arranges each value in resultlab into a manageable string file so it can be formatted and then written to a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

    #destroys the test results window and then re-opens the landing page.
    def rebegin(self):
        self.story.destroy()
        self.classinitagain()

    #ends the program after the tests results are shown, if the user chooses to close it by clicking the close button in the top-right of the window
    def final_close(self):
        if messagebox.askokcancel("Quitting the Program","Are you sure you don't want to perform any more tests?"):
            self.story.destroy()

    #shows the results in a text window
    def compile_results(self):
        self.flie = open(self.thisname, "r")
        self.st = self.flie.read()

        self.story = Tk()
        self.story.title("Results (DO NOT MAKE CHANGES TO THE TEXT AS THEY WILL NOT BE SAVED)")
        self.story.iconbitmap('aclogo.ico')
        self.story.geometry("800x600")

        self.textread = scrolledtext.ScrolledText(self.story,undo=True)
        self.textread.pack(expand=True, fill='both')
        self.textread.insert(INSERT, self.st)
        
        Button(self.story,text="New Test",command=self.rebegin).pack()

        self.story.mainloop()

    #shows how many tests a student has done
    def tcounter(self,val):
        self.lisstr = val.split(" ",1)
        c.execute('''SELECT TestCount FROM Subject WHERE Forename=? AND Surname=?''',(self.lisstr[0],self.lisstr[1],))
        self.tests = c.fetchall()
        if self.tests[0][0] == 0:
            self.desclab.configure(text="No assessments performed on this student so far.")
        elif self.tests[0][0] == 1:
            self.desclab.configure(text="1 assessment performed on this student so far.")
        elif self.tests[0][0] > 1:
            self.desclab.configure(text="{} assessments performed on this student so far.".format(self.tests[0][0]))
        
    #displays a notice if the webcam test is selected at any time
    def retext(self,val):
        if val == "Listening Skills (with webcam)":
            messagebox.showinfo("Notice for Webcam Test","PLEASE NOTE: The test will use your computer's built in webcam to monitor the student's face and eyes.\nIt is best to do this test in a bright room without many people in it.\nThe program will NOT record or store video footage from your webcam.\nThere is also an option of a listening test without a webcam. If you are still worried about choosing this option, choose the other one instead. You can also choose both the webcam and non-webcam tests.",icon="info")
        elif val == "Listening Skills (without webcam)":
            messagebox.showinfo("Notice for Listening Test", "PLEASE NOTE: You must NOT include any punctuation in your responses whatsoever.\nThere is also a test available, where you can use the webcam. It will monitor the subject's face and eyes.\nYou can also perform both tests in an assessment.",icon="info")
            
    #the actual process that adds a student to the database
    def writestud(self):
        self.initlist = self.lake
        self.first = self.ento1.get()
        self.last = self.ento2.get()
        if self.first == "" or self.last == "" or self.first.split(" ",1)[0] == '' or self.last.split(" ",1)[0] == '':
            messagebox.showerror("Please enter actual data","Please add both the student's first and last names and try again.")
        else:
            c.execute('''SELECT Forename, Surname FROM Subject WHERE Forename=? AND Surname=?''',(self.first,self.last,))
            self.check = c.fetchall()
            if self.check:
                messagebox.showerror("Student already in database","There is already a student of the same name in this database.")
            else:
                if len(self.first.split(" ")) >= 2:
                    messagebox.showerror("Please do not put spaces between students' first names","Please do not put spaces between a student's first name. Use hyphens where appropriate.")
                else:
                    c.execute('''INSERT INTO Subject(Forename, Surname, TestCount) VALUES (?,?,?)''',(self.first,self.last,int(0),))
                    db.commit()
                    messagebox.showinfo("Student Added", "A new student has been added to the database, which can now perform tests.\nSelect the same or a different student from the appropriate dropdown menu to have them perform the test. Then select your options.",icon="info")
                    if self.initlist == []:
                        self.lake == self.listmake([])
                    try:
                        self.prog.destroy()
                        self.master.destroy()
                        self.studins.destroy()
                        self.classinitagain()
                    except:
                        self.master.destroy()
                        self.studins.destroy()
                        self.classinitagain()

    #creates the window for inserting a student's name
    def studinsert(self):
        self.studins = Tk()
        self.studins.title("Add a Student to the AC Database")
        self.studins.iconbitmap('aclogo.ico')
        self.studins.geometry("500x250")

        self.intro = Label(self.studins, text="Please enter the student's name and surname here\nPlease don't seperate first names (use hyphens where applicable or needed)")
        self.labo1 = Label(self.studins, text="First Name")
        self.ento1 = Entry(self.studins)
        self.labo2 = Label(self.studins, text="Last Name")
        self.ento2 = Entry(self.studins)
        self.labo3 = Label(self.studins)
        self.proco = Button(self.studins, text="Proceed", command=self.writestud)
        
        self.intro.pack()
        self.labo1.pack()
        self.ento1.pack()
        self.labo2.pack()
        self.ento2.pack()
        self.labo3.pack()
        self.proco.pack()

        self.studins.mainloop()

    #creates the Student List window, for browsing the Student/Subject table in a separate window to the landing page
    def studlist(self):
        if self.lake == []:
            messagebox.showerror("No students available","There are no students in the database.\nClick \"Add New Student\" to add students to the database.")
        else:
            self.prog = Toplevel()
            self.prog.iconbitmap('aclogo.ico')
            self.prog.geometry("640x480")
            self.prog.title("Test Archive")
            self.labo = Label(self.prog,text="Filter by Student")
            self.say = StringVar(self)
            self.say.set("Select a student")
            self.drop = OptionMenu(self.prog,self.say,*self.lake,command=self.findtest)
            self.labo.pack()
            self.drop.pack()
            self.prog.mainloop()

    #shows the results of past tests
    def testload(self,val):
        c.execute('''SELECT Feedback FROM Test WHERE DateDone=?''',(val,))
        self.connection = c.fetchall()
        self.thisname = self.connection[0][0]
        try:
            
            self.flie = open(self.thisname, "r")
            self.st = self.flie.read()

            self.story = Tk()
            self.story.title("Test Feedback (DO NOT MAKE CHANGES TO THE TEXT AS THEY WILL NOT BE SAVED)")
            self.story.iconbitmap('aclogo.ico')
            self.story.geometry("800x600")

            self.textread = scrolledtext.ScrolledText(self.story,undo=True)
            self.textread.pack(expand=True, fill='both')
            self.textread.insert(INSERT, self.st)
            
            Button(self.story,text="Close",command=self.story.destroy).pack()

            self.story.mainloop()

        except FileNotFoundError:
            messagebox.showerror("File not there","The results file may have been deleted.")

    #gives a list of tests done by a student when a student is selected
    def findtest(self,val):
        if self.one:
            self.listoftests = []
            self.stream = StringVar(self)
            self.stream.set("Select a test")
            self.studname = val
            self.studio = self.studname.split(" ",1)
            self.firststud = self.studio[0]
            self.laststud = self.studio[1]
            try:
                c.execute('''SELECT ID From Subject WHERE Forename=? AND Surname=?''',(self.firststud,self.laststud,))
                self.stu_names = c.fetchall()
                self.st_id = self.stu_names[0][0]
                c.execute('''SELECT DateDone FROM Test WHERE SubjectID=?''',(self.st_id,))
                self.listdetails = c.fetchall()
                for i in range(0,len(self.listdetails)):
                    self.listoftests.append(self.listdetails[i][0])
                self.noon = Label(self.prog,text="Now select a test results file from this list")
                self.noon.pack()
                self.news = OptionMenu(self.prog,self.stream,*self.listoftests,command=self.testload)
                self.news.pack()
            except:
                try:
                    self.noon.pack_forget()
                    messagebox.showerror("No tests for this student","The student hasn't done any tests yet.\nEither select a different student, add a new student or do a test with a student.")
                except:
                    messagebox.showerror("No tests for this student","The student hasn't done any tests yet.\nEither select a different student, add a new student or do a test with a student.")
            self.one = False
        else:
            try:
                self.news.pack_forget()
                self.noon.pack_forget()
                self.one = True
                self.findtest(val)
            except:
                self.noon.pack_forget()
                self.one = True
                self.findtest(val)

#creates the SignApp GUI class, which logs in or registers the user.
class SignApp(Frame):
    #initiates the class's initial properties
    def __init__(self, master):
        super(SignApp,self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.pack()
        self.create()

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this? You haven't even started a test yet!"):
            self.master.destroy()
        
    #initiates the initial login/register GUI
    def create(self):
        self.empty = Label(self,text="")
        self.lab1 = Label(self, text="Username")
        self.lab1.pack()
        self.ent1 = Entry(self)
        self.ent1.pack()
        self.lab2 = Label(self, text="Password")
        self.lab2.pack()
        self.ent2 = Entry(self, show="•")
        self.ent2.pack()
        
        self.startlab = Label(self, text="Please choose one option to proceed")
        self.signin = Button(self, text="Login", command=self.find_sign)
        self.signup = Button(self, text="Register", command=self.new_sign)

        self.startlab.pack()
        self.signin.pack()
        self.signup.pack()

    #searches the Supervisor table for the user
    def find_sign(self):
        self.getuser = self.ent1.get()
        self.getpass = self.ent2.get()
        if self.getuser == "" or self.getuser == "" or self.getuser.split(" ",1)[0] == '' or self.getpass.split(" ",1)[0] == '':
            messagebox.showerror("Please enter actual data", "Please enter an actual username and password, and try again.")
        else:
            fndscrpt = 'SELECT Username, Password FROM Supervisor WHERE Username=? AND Password=?'
            c.execute(fndscrpt,(self.getuser,self.getpass,))
            details = c.fetchall()
            if details:
                messagebox.showinfo("Welcome to AC Assessments!", "You are now logged in and are able to access AC soft skills!", icon="info")
                fndscrpt = 'SELECT Forename, Surname FROM Supervisor WHERE Username=? AND Password=?'
                c.execute(fndscrpt,(self.getuser,self.getpass,))
                details = c.fetchall()
                self.getname = details[0][0]
                self.getsure = details[0][1]
                self.Main(self.getname,self.getsure)
            else:
                messagebox.showerror("Username not found","Please reenter your login details and try again.")

    #actually adds the user to the Supervisor table
    def write_sign(self):
        self.getuser = self.ent1.get()
        self.getpass = self.ent2.get()
        self.getname = self.ento1.get()
        self.getsure = self.ento2.get()
        c.execute('SELECT Forename, Surname FROM Supervisor WHERE Forename=? AND Surname=?',(self.getname,self.getsure,))
        det2 = c.fetchall()
        if self.getname == "" or self.getsure == "" or self.getname.split(" ",1)[0] == '' or self.getsure.split(" ",1)[0] == '':
            messagebox.showerror("Please enter actual data","Please add both your first and last names and try again.")
        elif det2:
            messagebox.showerror("Name used already","A user already has the same first and last names as you.\nPlease enter different ones and try again.")
        else:
            c.execute('''INSERT INTO Supervisor(Forename, Surname, Username, Password) VALUES (?,?,?,?)''',(self.getname,self.getsure,self.getuser,self.getpass,))
            db.commit()
            messagebox.showinfo("Welcome to AC Assessments!", "You are now registered with our soft skills assessment service. The program will now launch, and you will now be able to access AC soft skills!", icon="info")
            self.sign.destroy()
            self.Main(self.getname,self.getsure)

    #asks the user for their first and last names, before registering them to the service
    def new_sign(self):
        self.getuser = self.ent1.get()
        self.getpass = self.ent2.get()
        c.execute('SELECT Username, Password FROM Supervisor WHERE Username=? OR Password=?',(self.getuser,self.getpass,))
        det1 = c.fetchall()
        if self.getuser == "" or self.getpass == "" or self.getuser.split(" ",1)[0] == '' or self.getpass.split(" ",1)[0] == '':
            messagebox.showerror("Please enter actual data", "Please enter an actual username and password, and try again.")
        elif det1:
            messagebox.showerror("Credentials used already","A user already has the same username and/or password as you.\nPlease enter different ones and try again.")
        else:
            self.sign = Tk()
            self.sign.geometry("500x250")
            self.sign.title("AC Corp Soft Skills Assessment Program Initiation")

            self.intro = Label(self.sign, text="To complete the registering process, please enter your name and surname here")
            self.labo1 = Label(self.sign, text="First Name")
            self.ento1 = Entry(self.sign)
            self.labo2 = Label(self.sign, text="Last Name")
            self.ento2 = Entry(self.sign)
            self.labo3 = Label(self.sign)
            self.proco = Button(self.sign, text="Proceed", command=self.write_sign)

            self.intro.pack()
            self.labo1.pack()
            self.ento1.pack()
            self.labo2.pack()
            self.ento2.pack()
            self.labo3.pack()
            self.proco.pack()

            self.sign.mainloop()

    #defines the next window to be opened by the program: the landing page
    def Main(self,getname,getsure):
        self.master.destroy()
        mixer.music.load("startsound.ogg")
        mixer.music.play()
        root = Tk()
        root.title("AC Soft Skills Test Selection")
        root.geometry("500x500")
        sign = SelectApp(root, getname, getsure)
        root.mainloop()
        
def Main(): #the Main program, stored as a function, which starts the sign program
    root = Tk()
    root.title("Welcome to the Soft Skills Assessment Program!")
    root.geometry("400x400")
    sign = SignApp(root)
    root.mainloop()

if __name__ == "__main__": #when running the program directly, do this:
    Main()
    db.close()
