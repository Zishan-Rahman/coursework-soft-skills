from tkinter import * #imports the tkinter module
from tkinter import ttk #imports the ttk submodule in tkinter
from tkinter import messagebox #imports the messagebox submodule in tkinter
from random import choice, randint #imports the choice and randint functions from the random module

#creates the Questionnaire (confidence) class.
class QuestionApp(Frame):
    #initiates the class's initial properties
    def __init__(self, master, filename):
        super(QuestionApp, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.count = 0
        self.countmax = 10
        self.filename = filename
        self.opener = open(filename,"r")
        self.statements = list(self.opener)
        self.attempts = []
        self.randlist = []
        self.resultlab = []
        self.pack()
        self.app()

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #initialises the questionnaire window
    def app(self):
        self.lab1 = Label(self, text="Answer the questions using the buttons provided")
        self.lab1.pack()
        self.lab2 = Label(self, text="Questions asked: " + str(self.count) + " out of " + str(self.countmax))
        self.lab2.pack()
        self.nacks = Label(self, text=self.choico())
        self.nacks.pack()

        self.but1 = Button(self, text="Always Agree")
        self.but2 = Button(self, text="Agree")
        self.but3 = Button(self, text="I'm not exactly sure")
        self.but4 = Button(self, text="Disagree")
        self.but5 = Button(self, text="Always Disagree")

        self.but1.configure(command=lambda: self.buttons(self.but1))
        self.but2.configure(command=lambda: self.buttons(self.but2))
        self.but3.configure(command=lambda: self.buttons(self.but3))
        self.but4.configure(command=lambda: self.buttons(self.but4))
        self.but5.configure(command=lambda: self.buttons(self.but5))

        for i in [self.but1, self.but2, self.but3, self.but4, self.but5]:
            i.pack()

    #selects a random statement from the file
    def choico(self):
        randst = choice(self.statements).strip()
        while randst in self.randlist:
            randst = choice(self.statements).strip()   
        self.randlist.append(randst)
        return randst

    #creates an exit button if the limit is reached
    def exitbutton(self):
        if self.count >= self.countmax:
            self.end()
            self.but6 = Button(self, text="Exit", command=self.kill)
            self.but6.pack()

    #adds the selected response to the attempts dictionary to be added to the final results in a different form
    def buttons(self,botun):
        if self.count < self.countmax:
            self.count += 1
            self.lab2['text'] = "Questions asked: " + str(self.count) + " out of " + str(self.countmax)

            self.dicto = dict([('Number',self.count),('Question',self.nacks['text']),('Response',botun['text'])])
            self.attempts.append(self.dicto)
            
            self.nacks['text'] = self.choico()

            self.exitbutton()

    #closes the window (function reserved for the exit button at the end)
    def kill(self):
        self.master.destroy()

    #adds the details in the attempts array to a stringed form in resultlab
    def end(self):
        for i in range(len(self.attempts)):
            self.resultlab.append("Question {0}: {1}\nYou responded: {2}\n".format(self.attempts[i]['Number'],self.attempts[i]['Question'],self.attempts[i]['Response']))

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#creates the organisation class
class OrganisationApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(OrganisationApp, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.resultlab = []
        self.select = randint(1,3)
        self.pack()
        if self.select == 1:
            self.FireDrill()
        elif self.select == 2:
            self.PlanDay()
        elif self.select == 3:
            self.Revise()

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #confirms whether the user wants to send this data through and end the test
    def confirm(self):
        confirmation = messagebox.askquestion("Confirm responses","Are you sure you want to send this data through?",icon="question")
        if confirmation == "yes":
            self.retreive()
        else:
            None

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

    #retreives the answers from the drop-down menus and then appends them to resultlab
    #through a specific function that depends on which topic was randomly selected
    def retreive(self):
        self.ans1 = self.dr1store.get()
        self.ans2 = self.dr2store.get()
        self.ans3 = self.dr3store.get()
        self.correctans = 0

        if self.select == 1:
            self.fireanswer()
        elif self.select == 2:
            self.plananswer()
        elif self.select == 3:
            self.reviseanswer()

    #loads the "fire drill" questionnaire if it's randomly selected
    def FireDrill(self):
        self.labtitle = Label(self,text="Topic for this test: The Fire Drill")
        self.labtitle.pack()

        self.q1 = Label(self,text="The Fire Alarm has just gone off. What do you do?")
        self.q1.pack()

        self.ac = ["Get Coats and Bags","Look for Friends","Head to Central Meeting Point","Line up in groups","Leave building immediately"]
        self.dr1store = StringVar(self)
        self.dr1store.set("Select one")
        self.dr2store = StringVar(self)
        self.dr2store.set("Select one")
        self.dr3store = StringVar(self)
        self.dr3store.set("Select one")

        for i in (self.dr1store,self.dr2store,self.dr3store):
            OptionMenu(self,i,*self.ac).pack()

        self.botexit = Button(self,text="Submit",command=self.confirm)
        self.botexit.pack()

    #loads the "planning day" questionnaire if it's randomly selected
    def PlanDay(self):
        self.labtitle = Label(self,text="Topic for this test: Planning in the night for the day ahead")
        self.labtitle.pack()

        self.q1 = Label(self,text="Before you go to bed, what should you do before planning for the next day?")
        self.q1.pack()

        self.ac = ["Pack all your bags the night before",
                   "Check timetable to ensure you have packed the correct books",
                   "Go to bed very late",
                   "Talk to a friend late in the night",
                   "Pack your pencil case and put it in the bag"]
        self.dr1store = StringVar(self)
        self.dr1store.set("Select one")
        self.dr2store = StringVar(self)
        self.dr2store.set("Select one")
        self.dr3store = StringVar(self)
        self.dr3store.set("Select one")

        for i in (self.dr1store,self.dr2store,self.dr3store):
            OptionMenu(self,i,*self.ac).pack()

        self.botexit = Button(self,text="Submit",command=self.confirm)
        self.botexit.pack()        

    #loads the "planning revision" questionnaire if it's randomly selected
    def Revise(self):
        self.labtitle = Label(self,text="Topic for this test: What to do when you REVISE")
        self.labtitle.pack()

        self.q1 = Label(self,text="What do you need to do when you revise?")
        self.q1.pack()

        self.ac = ["Allocate a set amount of time for revision",
                   "Take Regular Breaks",
                   "Take very very very long sleeps",
                   "Watch TV for no justifiable reason",
                   "Make a revision timetable"]
        self.dr1store = StringVar(self)
        self.dr1store.set("Select one")
        self.dr2store = StringVar(self)
        self.dr2store.set("Select one")
        self.dr3store = StringVar(self)
        self.dr3store.set("Select one")

        for i in (self.dr1store,self.dr2store,self.dr3store):
            OptionMenu(self,i,*self.ac).pack()

        self.botexit = Button(self,text="Submit",command=self.confirm)
        self.botexit.pack()    

    #checks for the right answers in the right order, and adds all results to resultlab, for the "fire drill" questionnaire
    def fireanswer(self):
        if self.ans1 == "Leave building immediately":
            self.correctans += 1
        if self.ans2 == "Head to Central Meeting Point":
            self.correctans += 1
        if self.ans3 == "Line up in groups":
            self.correctans += 1

        if self.correctans == 3:
            self.stane = "Your order and selections were fully correct"
        else:
            self.stane = "Your order and selections were not fully correct"

        self.resultlab.append("""{0}
Question: {1}
Your responses: {2}, {3}, {4}
Correct responses: Leave building immediately, Head to Central Meeting Point, Line up in groups
Correct ordered responses: {5} out of 3
{6}""".format(self.labtitle['text'],self.q1['text'],self.ans1,self.ans2,self.ans3,self.correctans,self.stane))

        self.master.destroy()

    #checks for the right answers in the right order, and adds all results to resultlab, for the "planning day" questionnaire
    def plananswer(self):
        if self.ans1 == "Pack your pencil case and put it in the bag":
            self.correctans += 1
        if self.ans2 == "Check timetable to ensure you have packed the correct books":
            self.correctans += 1
        if self.ans3 == "Pack all your bags the night before":
            self.correctans += 1

        if self.correctans == 3:
            self.stane = "Your order and selections were fully correct"
        else:
            self.stane = "Your order and selections were not fully correct"

        self.resultlab.append("""{0}
Question: {1}
Your responses: {2}, {3}, {4}
Correct responses: Pack your pencil case and put it in the bag, Check timetable to ensure you have packed the correct books, Pack all your bags the night before
Correct ordered responses: {5} out of 3
{6}""".format(self.labtitle['text'],self.q1['text'],self.ans1,self.ans2,self.ans3,self.correctans,self.stane))

        self.master.destroy()

    #checks for the right answers in the right order, and adds all results to resultlab, for the "planning revision" questionnaire
    def reviseanswer(self):
        if self.ans1 == "Make a revision timetable":
            self.correctans += 1
        if self.ans2 == "Allocate a set amount of time for revision":
            self.correctans += 1
        if self.ans3 == "Take Regular Breaks":
            self.correctans += 1

        if self.correctans == 3:
            self.stane = "Your order and selections were fully correct"
        else:
            self.stane = "Your order and selections were not fully correct"

        self.resultlab.append("""{0}
Question: {1}
Your responses: {2}, {3}, {4}
Correct responses: Make a revision timetable, Allocate a set amount of time for revision, Take Regular Breaks
Correct ordered responses: {5} out of 3
{6}""".format(self.labtitle['text'],self.q1['text'],self.ans1,self.ans2,self.ans3,self.correctans,self.stane))

        self.master.destroy()

#creates the motivation class
class MotivApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(MotivApp, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.attempts = []
        self.resultlab = []
        self.pack()
        self.app()

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #creates the questionnaire, displaying all widgets for each question in the window
    def app(self):
        self.lab1 = Label(self,text="Answer the below 5 questions about the topic of motivation.")
        self.lab1.pack()
        
        self.q1 = Label(self,text="What motivates you?")
        self.q1.pack()
        self.ent1 = Entry(self,width=30)
        self.ent1.pack()

        self.q2 = Label(self,text="What times of the day are you most motivated (if other, please specify)?")
        self.q2.pack()
        self.lista = ["All of the time", "Sometimes", "None of the time", "In the morning", "When I wake up", "In the afternoon", "When I am working", "When I have fun", "In the evening", "In the night", "Other"]
        self.dr1 = StringVar(self)
        self.dr1.set("Other")
        self.drop1 = OptionMenu(self,self.dr1,*self.lista,command=self.store1)
        self.drop1.pack()
        self.oth1 = Label(self,text="Other/Additional Information")
        self.oth1.pack()
        self.ent2 = Entry(self,width=30)
        self.ent2.pack()

        self.q3 = Label(self,text="How do you motivate yourself when you're feeling unmotivated?")
        self.q3.pack()
        self.ent3 = Entry(self,width=30)
        self.ent3.pack()

        self.q4 = Label(self,text="Do you struggle with motivation (click one to select)?")
        self.q4.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        self.yes_ans = Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2)
        self.yes_ans.pack()
        self.no_ans = Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2)
        self.no_ans.pack()

        self.q5 = Label(self,text="Are you motivated by rewards (click one to select)?")
        self.q5.pack()
        self.dr3 = StringVar(self)
        self.dr3.set("")
        self.yes_ans = Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3)
        self.yes_ans.pack()
        self.no_ans = Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3)
        self.no_ans.pack()
        Label(self,text="").pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

    #confirms whether the user wants to send this data through and end the test
    def confirm(self):
        confirmation = messagebox.askquestion("Confirm responses","Are you sure you want to send this data through?",icon="question")
        if confirmation == "yes":
            self.end()
        else:
            None

    #takes each question and answer given, and appends all to resultlab
    def end(self):
        self.resultlab.append("Question 1: What motivates you?\nYour response: {}\n".format(self.ent1.get().lower().strip()))
        self.resultlab.append("Question 2: What times of the day are you most motivated?\nYour response: {}\nOther/Additional information entered: {}\n".format(self.dr1store.lower().strip(),self.ent2.get().lower().strip()))
        self.resultlab.append("Question 3: How do you motivate yourself when you're feeling unmotivated?\nYour response: {}\n".format(self.ent3.get().lower().strip()))
        self.resultlab.append("Question 4: Do you struggle with motivation?\nYour response: {}\n".format(self.dr2store))
        self.resultlab.append("Question 5: Are you motivated by rewards?\nYour response: {}\n".format(self.dr3store))
        self.master.destroy()

    #stores the response given for question 2
    def store1(self,val):
        self.dr1store = val

    #stores the response given for question 4
    def store2(self):
        self.dr2store = self.dr2.get()

    #stores the response given for question 5
    def store3(self):
        self.dr3store = self.dr3.get()

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#creates the self-awareness class, which inherits from the motivation class
class SelfAwareApp(MotivApp):
    #initiates the class's initial properties
    def __init__(self,master):
        super(MotivApp, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.attempts = []
        self.resultlab = []
        self.pack()
        self.app()

    #creates the actual questionnaire, with the relevant widgets displayed and data retrieval methods selected
    def app(self):
        Label(self,text="Click on each radio button to select a response.\nOnce you click on one, it will be selected.\n").pack()
        
        self.dr1 = StringVar(self)
        self.dr1.set("")
        self.dr2 = StringVar(self)
        self.dr2.set("")
        self.dr3 = StringVar(self)
        self.dr3.set("")
        self.dr4 = StringVar(self)
        self.dr4.set("")
        self.dr5 = StringVar(self)
        self.dr5.set("")
        self.dr6 = StringVar(self)
        self.dr6.set("")

        self.lab1 = Label(self,text="Do you recognise when you're not feeling yourself (i.e. feeling different)?")
        self.lab2 = Label(self,text="Do you pay attention to how you react to different situations?")
        self.lab3 = Label(self,text="Do you try and manage yourself and your behaviours?")
        self.lab4 = Label(self,text="Are you able to ask yourself why you think about or do something?")
        self.lab5 = Label(self,text="Are you able to tell when what you do isn't giving you what you want?")
        self.lab6 = Label(self,text="Are you able to recognise when your actions are either wrong or harmful (or both)?")

        self.lab1.pack()
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()
        self.lab2.pack()
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()
        self.lab3.pack()
        Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3).pack()
        Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3).pack()
        self.lab4.pack()
        Radiobutton(self,text="Yes",variable=self.dr4,value="Yes",command=self.store4).pack()
        Radiobutton(self,text="No",variable=self.dr4,value="No",command=self.store4).pack()
        self.lab5.pack()
        Radiobutton(self,text="Yes",variable=self.dr5,value="Yes",command=self.store5).pack()
        Radiobutton(self,text="No",variable=self.dr5,value="No",command=self.store5).pack()
        self.lab6.pack()
        Radiobutton(self,text="Yes",variable=self.dr6,value="Yes",command=self.store6).pack()
        Radiobutton(self,text="No",variable=self.dr6,value="No",command=self.store6).pack()

        Label(self,text="").pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

    #gets the response selected for question 1 (questions 2 and 3 have methods inherited from the MotivApp class)
    def store1(self):
        self.dr1store = self.dr1.get()

    #gets the response selected for question 4
    def store4(self):
        self.dr4store = self.dr4.get()

    #gets the response selected for question 5
    def store5(self):
        self.dr5store = self.dr5.get()

    #gets the response selected for question 6
    def store6(self):
        self.dr6store = self.dr6.get()

    #gets the answers selected for each question, then closes the window
    def end(self):
        self.resultlab.append("Question 1: {}\nYour response: {}\n".format(self.lab1['text'],self.dr1store))
        self.resultlab.append("Question 2: {}\nYour response: {}\n".format(self.lab2['text'],self.dr2store))
        self.resultlab.append("Question 3: {}\nYour response: {}\n".format(self.lab3['text'],self.dr3store))
        self.resultlab.append("Question 4: {}\nYour response: {}\n".format(self.lab4['text'],self.dr4store))
        self.resultlab.append("Question 5: {}\nYour response: {}\n".format(self.lab5['text'],self.dr5store))
        self.resultlab.append("Question 6: {}\nYour response: {}\n".format(self.lab6['text'],self.dr6store))
        self.master.destroy()

#creates the social skills class
class SocSkills(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(SocSkills, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.resultlab = []
        self.pack()
        self.app()

    #creates the actual questionnaire, with relevant widgets and means to retrieve data
    def app(self):
        self.q1 = Label(self, text="How do you start a conversation?")
        self.q1.pack()
        self.ac1 = ['Say "hello"','Say "no"','Stare at them', 'Turn your back to them', 'Give them a big fright!']
        self.dr1 = StringVar(self)
        self.dr1.set("Select One")
        self.drop1 = OptionMenu(self,self.dr1,*self.ac1)
        self.drop1.pack()

        self.q2 = Label(self, text="When it comes to listening skills, what must you do with your eyes?")
        self.q2.pack()
        self.ac2 = ['Stare','Don\'t stare, but maintain eye contact at least 70% of the time', 'Don\'t even look at them']
        self.dr2 = StringVar(self)
        self.dr2.set("Select One")
        self.drop2 = OptionMenu(self,self.dr2,*self.ac2)
        self.drop2.pack()

        self.q3 = Label(self, text="During a conversation, you should ask questions based on...")
        self.q3.pack()
        self.ac3 = ['What you heard (from the others in the conversation)','How they are','Make it all about you']
        self.dr3 = StringVar(self)
        self.dr3.set("Select One")
        self.drop3 = OptionMenu(self,self.dr3,*self.ac3)
        self.drop3.pack()

        self.q4 = Label(self, text="When it comes to body language, what should you do?")
        self.q4.pack()
        self.ac4 = ['Slouch','Fiddle with something','Yawn (very loudly)','Stand or Sit Up Straight']
        self.dr4 = StringVar(self)
        self.dr4.set("Select One")
        self.drop4 = OptionMenu(self,self.dr4,*self.ac4)
        self.drop4.pack()

        self.q5 = Label(self, text="What is the best way of taking turns?")
        self.q5.pack()
        self.ac5 = ['ALL ME ME ME','ALL YOU YOU YOU','One-at-a-time','Wait for others and judge when it\'s appropriate to join']
        self.dr5 = StringVar(self)
        self.dr5.set("Select One")
        self.drop5 = OptionMenu(self,self.dr5,*self.ac5)
        self.drop5.pack()

        self.q6 = Label(self, text="When it comes to facial expressions, should you be paying attention to the expressions the others make?")
        self.q6.pack()
        self.ac6 = ['Yes','No']
        self.dr6 = StringVar(self)
        self.dr6.set("Select One")
        self.drop6 = OptionMenu(self,self.dr6,*self.ac6)
        self.drop6.pack()

        self.q7 = Label(self, text="If someone is frowning, for instance, how might they be feeling?")
        self.q7.pack()
        self.ac7 = ['Excited','Sad or Depressed','Happy','Angry']
        self.dr7 = StringVar(self)
        self.dr7.set("Select One")
        self.drop7 = OptionMenu(self,self.dr7,*self.ac7)
        self.drop7.pack()

        self.botone = Button(self,text="Pass in",command=self.confirm)
        self.botone.pack()
    
    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #adds all the results to resultlab, with appropraite corrections, then closes the window
    def end(self):
        self.correctans = 0
        self.dr1store = self.dr1.get()
        self.dr2store = self.dr2.get()
        self.dr3store = self.dr3.get()
        self.dr4store = self.dr4.get()
        self.dr5store = self.dr5.get()
        self.dr6store = self.dr6.get()
        self.dr7store = self.dr7.get()

        if self.dr1store == 'Say "hello"':
            self.correctans += 1
        if self.dr2store == 'Don\'t stare, but maintain eye contact at least 70% of the time':
            self.correctans += 1
        if self.dr3store == 'What you heard (from the others in the conversation)':
            self.correctans += 1
        if self.dr4store == 'Stand or Sit Up Straight':
            self.correctans += 1
        if self.dr5store == 'Wait for others and judge when it\'s appropriate to join':
            self.correctans += 1
        if self.dr6store == 'Yes':
            self.correctans += 1
        if self.dr7store == 'Sad or Depressed':
            self.correctans += 1

        self.correct = ('Say "hello"',
                        'Don\'t stare, but maintain eye contact at least 70% of the time',
                        'What you heard (from the others in the conversation)',
                        'Stand or Sit Up Straight',
                        'Wait for others and judge when it\'s appropriate to join',
                        'Yes',
                        'Sad or Depressed')
                        
        self.results = ((self.q1['text'],self.dr1store),
                        (self.q2['text'],self.dr2store),
                        (self.q3['text'],self.dr3store),
                        (self.q4['text'],self.dr4store),
                        (self.q5['text'],self.dr5store),
                        (self.q6['text'],self.dr6store),
                        (self.q7['text'],self.dr7store))

        for i in range(0,len(self.results)):
            self.resultlab.append("Question {}: {}\nYou responded: {}\nCorrect Response: {}\n".format(i+1,self.results[i][0],self.results[i][1],self.correct[i]))
        self.resultlab.append("{} of {} correct".format(self.correctans,len(self.correct)))

        self.master.destroy()
            
    #confirms whether the user wants to send this data through and end the test
    def confirm(self):
        confirmation = messagebox.askquestion("Confirm responses","Are you sure you want to send this data through?",icon="question")
        if confirmation == "yes":
            self.end()
        else:
            None

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

#creates the life skills class
class LifeApp(Frame):
    #initiates the class's initial properties
    def __init__(self,master,test_name):
        super(LifeApp, self).__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.test_name = test_name
        self.attempts = []
        self.resultlab = []
        self.pack()
        if self.test_name == "Money":
            self.MoneyApp()
        elif self.test_name == "Strangers":
            self.StrangerApp()
        elif self.test_name == "Cooking":
            self.CookApp()
        elif self.test_name == "Shopping":
            self.ShopApp()
        elif self.test_name == "Self-Care":
            self.SelfCareApp()

    #confirms whether the user wants to send this data through and end the test
    def confirm(self):
        confirmation = messagebox.askquestion("Confirm responses","Are you sure you want to send this data through?",icon="question")
        if confirmation == "yes":
            self.end()
        else:
            None

    #adapts the data in resultlab into a string to be added to the results at the end of the whole assessment, in the form of a text file
    def file(self):
        self.endreturn = ""
        for i in self.resultlab:
            self.endreturn += i
        return self.endreturn

    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #retrieves the answer given to the first question
    def store1(self):
        self.dr1store = self.dr1.get()

    #retrieves the answer given to the second question
    def store2(self):
        self.dr2store = self.dr2.get()

    #retrieves the answer given to the third question
    def store3(self):
        self.dr3store = self.dr3.get()

    #retrieves the answer given to the fourth question
    def store4(self):
        self.dr4store = self.dr4.get()

    #retrieves the answer given to the fifth question
    def store5(self):
        self.dr5store = self.dr5.get()

    #retrieves the answer given to the sixth question
    def store6(self):
        self.dr6store = self.dr6.get()

    #appends the values in the respective answer variables to resultlab and then closes the window
    def end(self):
        if self.test_name == "Money":
            self.resultlab.append("Topic selected: Money\n")
            self.resultlab.append("Question 1: How do you manage your money?\nYou responded: {}\n".format(self.ent1.get()))
            self.resultlab.append("Question 2: Do you have your own bank account?\nYou responded: {}\n".format(self.dr1store))
            self.resultlab.append("Question 3: Do you have any savings?\nYou responded: {}\n".format(self.dr2store))
            self.resultlab.append("Question 4: How do you work out how much to save (and/or spend)?\nYou responded: {}\n".format(self.ent4.get()))
            self.resultlab.append("Question 5: How do you use your money?\nYou responded: {}\n".format(self.ent5.get()))
        elif self.test_name == "Strangers":
            self.resultlab.append("Topic selected: Strangers\n")
            self.resultlab.append("Question 1: Would you get in a car with someone you don't know (even an Uber or other cab)?\nYou responded: {}\n".format(self.dr1store))
            self.resultlab.append("Question 2: Would you accept money and/or deeds for/from someone you don't know?\nYou responded: {}\n".format(self.dr2store))
            self.resultlab.append("Question 3: Would you talk to someone you don't know?\nYou responded: {}\n".format(self.dr3store))
            self.resultlab.append("Question 4: Would you give your phone number to someone you don't know (and/or take theirs)?\nYou responded: {}\n".format(self.dr4store))
        elif self.test_name == "Cooking":
            self.resultlab.append("Topic selected: Cooking\n")
            self.resultlab.append("Question 1: Can you cook a meal for yourself?\nYou responded: {}\n".format(self.dr1store))
            self.resultlab.append("Question 2: Can you cook for others?\nYou responded: {}\n".format(self.dr2store))
            self.resultlab.append("Question 3: Can you cook with others?\nYou responded: {}\n".format(self.dr3store))
            self.resultlab.append("Question 4: Can you follow a recipe\nYou responded: {}\n".format(self.dr4store))
            self.resultlab.append("Question 5: Do you know how to handle a stove/hob?\nYou responded: {}\n".format(self.dr5store))
        elif self.test_name == "Shopping":
            self.resultlab.append("Topic selected: Shopping\n")
            self.resultlab.append("Question 1: Can you spend wisely?\nYou responded: {}\n".format(self.dr1store))
            self.resultlab.append("Question 2: Can you travel on your own to the shops?\nYou responded: {}\n".format(self.dr2store))
            self.resultlab.append("Question 3: Can you navigate around a shopping street, mall or district?\nYou responded: {}\n".format(self.dr3store))
            self.resultlab.append("Question 4: Can you create and follow a shopping list?\nYou responded: {}\n".format(self.dr4store))
            self.resultlab.append("Question 5: Can you use a trolley?\nYou responded: {}\n".format(self.dr5store))
        elif self.test_name == "Self-Care":
            self.resultlab.append("Topic selected: Self-Care\n")
            self.resultlab.append("Question 1: Can you bath/shower yourself?\nYou responded: {}\n".format(self.dr1store))
            self.resultlab.append("Question 2: Can you travel independently (to most local places, for example)?\nYou responded: {}\n".format(self.dr2store))
            self.resultlab.append("Question 3: Can you plan your day and/or life effectively?\nYou responded: {}\n".format(self.dr3store))
            self.resultlab.append("Question 4: Do you get enough sleep?\nYou responded: {}\n".format(self.dr4store))
            self.resultlab.append("Question 5: Do you do enough exercise?\nYou responded: {}\n".format(self.dr5store))
            self.resultlab.append("Qusetion 6: Do you have a social life?\nYou responded: {}\n".format(self.dr6store))
        self.master.destroy()

    #creates the Money questionnaire
    def MoneyApp(self):
        self.lab1 = Label(self,text="Topic for this test: Money")
        self.lab1.pack()
        
        self.q1 = Label(self,text="How do you manage your money?")
        self.q1.pack()
        self.ent1 = Entry(self,width=35)
        self.ent1.pack()

        self.q2 = Label(self,text="Do you have your own bank account?")
        self.q2.pack()
        self.dr1 = StringVar(self)
        self.dr1.set("")
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()

        self.q3 = Label(self,text="Do you have any savings?")
        self.q3.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()

        self.q4 = Label(self,text="How do you work out how much to save (and/or spend)?")
        self.q4.pack()
        self.ent4 = Entry(self,width=35)
        self.ent4.pack()

        self.q5 = Label(self,text="How do you use your money?")
        self.q5.pack()
        self.ent5 = Entry(self,width=35)
        self.ent5.pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()        

    #creates the Strangers questionnaire
    def StrangerApp(self):
        self.lab1 = Label(self,text="Topic for this test: Strangers")
        self.lab1.pack()        
        
        self.q1 = Label(self,text="Would you get in a car with someone you don't know (even an Uber or other cab)?")
        self.q1.pack()
        self.dr1 = StringVar(self)
        self.dr1.set("")
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()

        self.q2 = Label(self,text="Would you accept money and/or deeds for/from someone you don't know?")
        self.q2.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()
        
        self.q3 = Label(self,text="Would you talk to someone you don't know?")
        self.q3.pack()
        self.dr3 = StringVar(self)
        self.dr3.set("")
        Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3).pack()
        Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3).pack()

        self.q4 = Label(self,text="Would you give your phone number to someone you don't know (and/or take theirs)?")
        self.q4.pack()
        self.dr4 = StringVar(self)
        self.dr4.set("")
        Radiobutton(self,text="Yes",variable=self.dr4,value="Yes",command=self.store4).pack()
        Radiobutton(self,text="No",variable=self.dr4,value="No",command=self.store4).pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

    #creates the Cooking questionnaire
    def CookApp(self):
        self.lab1 = Label(self,text="Topic for this test: Cooking")
        self.lab1.pack()

        self.q1 = Label(self,text="Can you cook a meal for yourself?")
        self.q1.pack()
        self.dr1 = StringVar(self)
        self.dr1.set("")
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()

        self.q2 = Label(self,text="Can you cook for others?")
        self.q2.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()
        
        self.q3 = Label(self,text="Can you cook with others?")
        self.q3.pack()
        self.dr3 = StringVar(self)
        self.dr3.set("")
        Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3).pack()
        Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3).pack()

        self.q4 = Label(self,text="Can you follow a recipe?")
        self.q4.pack()
        self.dr4 = StringVar(self)
        self.dr4.set("")
        Radiobutton(self,text="Yes",variable=self.dr4,value="Yes",command=self.store4).pack()
        Radiobutton(self,text="No",variable=self.dr4,value="No",command=self.store4).pack()

        self.q5 = Label(self,text="Do you know how to handle a stove/hob?")
        self.q5.pack()
        self.dr5 = StringVar(self)
        self.dr5.set("")
        Radiobutton(self,text="Yes",variable=self.dr5,value="Yes",command=self.store5).pack()
        Radiobutton(self,text="No",variable=self.dr5,value="No",command=self.store5).pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

    #creates the Shopping questionnaire
    def ShopApp(self):
        self.lab1 = Label(self,text="Topic for this test: Shopping")
        self.lab1.pack()

        self.q1 = Label(self,text="Can you spend wisely?")
        self.q1.pack()
        self.dr1 = StringVar(self)
        self.dr1.set("")
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()

        self.q2 = Label(self,text="Can you travel on your own to the shops?")
        self.q2.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()
        
        self.q3 = Label(self,text="Can you navigate around a shopping street, mall or district?")
        self.q3.pack()
        self.dr3 = StringVar(self)
        self.dr3.set("")
        Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3).pack()
        Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3).pack()

        self.q4 = Label(self,text="Can you create and follow a shopping list?")
        self.q4.pack()
        self.dr4 = StringVar(self)
        self.dr4.set("")
        Radiobutton(self,text="Yes",variable=self.dr4,value="Yes",command=self.store4).pack()
        Radiobutton(self,text="No",variable=self.dr4,value="No",command=self.store4).pack()

        self.q5 = Label(self,text="Can you use a trolley?")
        self.q5.pack()
        self.dr5 = StringVar(self)
        self.dr5.set("")
        Radiobutton(self,text="Yes",variable=self.dr5,value="Yes",command=self.store5).pack()
        Radiobutton(self,text="No",variable=self.dr5,value="No",command=self.store5).pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

    #creates the Self-Care questionnaire
    def SelfCareApp(self):
        self.lab1 = Label(self,text="Topic for this test: Self-Care")
        self.lab1.pack()

        self.q1 = Label(self,text="Can you bath/shower yourself?")
        self.q1.pack()
        self.dr1 = StringVar(self)
        self.dr1.set("")
        Radiobutton(self,text="Yes",variable=self.dr1,value="Yes",command=self.store1).pack()
        Radiobutton(self,text="No",variable=self.dr1,value="No",command=self.store1).pack()

        self.q2 = Label(self,text="Can you travel independently (to most local places, for example)?")
        self.q2.pack()
        self.dr2 = StringVar(self)
        self.dr2.set("")
        Radiobutton(self,text="Yes",variable=self.dr2,value="Yes",command=self.store2).pack()
        Radiobutton(self,text="No",variable=self.dr2,value="No",command=self.store2).pack()
        
        self.q3 = Label(self,text="Can you plan your day and/or life effectively?")
        self.q3.pack()
        self.dr3 = StringVar(self)
        self.dr3.set("")
        Radiobutton(self,text="Yes",variable=self.dr3,value="Yes",command=self.store3).pack()
        Radiobutton(self,text="No",variable=self.dr3,value="No",command=self.store3).pack()

        self.q4 = Label(self,text="Do you get enough sleep?")
        self.q4.pack()
        self.dr4 = StringVar(self)
        self.dr4.set("")
        Radiobutton(self,text="Yes",variable=self.dr4,value="Yes",command=self.store4).pack()
        Radiobutton(self,text="No",variable=self.dr4,value="No",command=self.store4).pack()

        self.q5 = Label(self,text="Do you do enough exercise?")
        self.q5.pack()
        self.dr5 = StringVar(self)
        self.dr5.set("")
        Radiobutton(self,text="Yes",variable=self.dr5,value="Yes",command=self.store5).pack()
        Radiobutton(self,text="No",variable=self.dr5,value="No",command=self.store5).pack()

        self.q6 = Label(self,text="Do you have a social life?")
        self.q6.pack()
        self.dr6 = StringVar(self)
        self.dr6.set("")
        Radiobutton(self,text="Yes",variable=self.dr6,value="Yes",command=self.store6).pack()
        Radiobutton(self,text="No",variable=self.dr6,value="No",command=self.store6).pack()

        self.exitbotun = Button(self,text="Enter",command=self.confirm)
        self.exitbotun.pack()

#class the life skills topic selection class
class select_test(Frame):
    #initiates the class's initial properties
    def __init__(self,master):
        super(select_test,self).__init__(master)
        self.testchoice = ("Money","Strangers","Cooking","Shopping","Self-Care")
        self.master.protocol("WM_DELETE_WINDOW",self.confirmclosure)
        self.master.iconbitmap('aclogo.ico')
        self.pack()
        self.choico()
    
    #confirms whether the program will be closed when the top-right close button is clicked
    def confirmclosure(self):
        if messagebox.askokcancel("Quitting the program","Are you sure you want to close this test? Data entered will NEITHER be saved NOR be considered in the final assessment results!"):
            self.master.destroy()

    #allows the supervisor to select from 5 topic-specific questionnaires
    def choico(self):
        self.choice = StringVar()
        self.choice.set("")
        Label(self,text="Select a test from the 5 options below").pack()
        Label(self,text="").pack()
        for i in range(len(self.testchoice)):
            Radiobutton(self,text=self.testchoice[i],indicatoron=0,width=20,padx=20,variable=self.choice,value=self.testchoice[i]).pack()
        Label(self,text="").pack()
        self.starto = Button(self,text="Perform Test",command=self.perform)
        self.starto.pack()

    #gets the choice selected and closes the window
    def perform(self):
        self.selection = self.choice.get()
        self.master.destroy()

    #returns the selected choice
    def save(self):
        return self.selection

#function for the confidence questionnaire
def Mantra():
    root = Tk()
    root.title("Confidence Questionnaire")
    root.geometry("640x480")
    sign = QuestionApp(root, "Mantras.txt")
    root.mainloop()

    box = sign.file()
    return box

#function for the motivation questionnaire
def Motivation():
    root = Tk()
    root.title("Motivation Questionnaire")
    root.geometry("640x480")
    sign = MotivApp(root)
    root.mainloop()

    box = sign.file()
    return box

#function for the self-awareness questionnaire
def SelfAware():
    root = Tk()
    root.title("Self Awareness Questionnaire")
    root.geometry("800x600")
    sign = SelfAwareApp(root)
    root.mainloop()

    box = sign.file()
    return box

#function for the organisation questionnaire
def Organise():
    root = Tk()
    root.title("Organisation Questionnaire")
    root.geometry("640x480")
    sign = OrganisationApp(root)
    root.mainloop()

    box = sign.file()
    return box

#function for the social skills questionnaire
def Social():
    root = Tk()
    root.title("Social Skills Questionnaire")
    root.geometry("800x600")
    sign = SocSkills(root)
    sign.mainloop()

    box = sign.file()
    return box

#function for the life skills questionnaire selection and subsequent test
def LifeSkills():
    root = Tk()
    root.title("Choose the Topic")
    root.geometry("300x300")
    tide = select_test(root)
    root.mainloop()

    try:
        test_name = tide.save()
    except:
        return "This test has not been performed because an option hasn't been selected"

    root = Tk()
    root.title("Life Skills")
    root.geometry("800x600")
    sign = LifeApp(root,test_name)
    root.mainloop()

    box = sign.file()
    return box

if __name__ == "__main__": #when running the program directly, do this:
    print(LifeSkills())
