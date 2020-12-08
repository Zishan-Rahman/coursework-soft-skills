# AC Soft Skill Assessment Program

## A coursework project that was written for the assessment(s) of special needs students' soft skills

This was originally written (primarily by me) as a coursework project for the AQA Computer Science A-Level Course (code: 7517).

This is a Windows application for assessing a special needs student's soft skills. Soft skills are historically harder to assess than hard skills, but are just as, if not more, important in various aspects of life (i.e. work, study et cetera). Hence, this program was written as an attempt to mitigate these problems.

Changes to this program may or may not occur in the future, but apart from the requirements, readme and license files, and the vscode folder, everything else is as was submitted in early April 2020. There are also plans to test out more builds for platforms other than Windows (and APIs other than Win32).

## **DISCLAIMER**

**The software was primarily written as a coursework project and _MUST NOT_ be interpreted as scientific fact. This is by no means a perfect solution to assessing soft skills. In addition, this program doesn't have sufficient documentation (besides comments in the source code) as of late and, at the moment, no major development on this has occured in quite a while, so please do not interpret results from assessments held on this program as hardline evidence on students.**

### How to use AC Soft Skills

1. Either register yourself as a supervisor or, if you've already registered, login.
2. Once successful, you'll be taken to a landing page where you can select up to 5 tests.
3. Select the student and then the 5 tests.
   - You can select a test more than once, **but** the program will filter out the repeatedly selected tests so that only the first instance of that one test occurs.
   - If there are no students/subjects to select, or your specific student is not in the students list, click "Add New Student" to, well, add a new student to the list.
4. Once selected, click "Start Test" to start the test.
   - Each test will be intuitive and you should be able to know what to do just by looking at the GUI.
   - The tests vary from a listening test to some questionnaires. There's even a webcam test.
5. Once the test is over, there is an additional window for writing some additional notes. Once done, click the "Finish" button.
6. Then, you will be shown the test results. Once you've inspected them, click "New Test" to be redirected to the landing page.
7. To view past test, click "Test Archive" from the landing page. It will open a new window where you can select a student, then select a test from another drop-down menu.
8. To log out, so that another supervisor can either register or login, click "Log Out" to be redirected to the sign-in window.

### Requirements and Build Instructions

If you want to either build this yourself or run it without building it, Python will need to be installed onto your system (version 3.8 or higher). The program will use some of Python's built-in libraries, including tkinter for creating the GUI.  

Additionally, the program requires some external packages in order to process certain functions:  
- opencv-python (for the webcam test)  
- NumPy (for use with opencv-python in the webcam test)  
- Pillow (for showing the map and timetable images)  
- cx_Freeze ((optional) for building the EXE file)  
- py2exe ((optional) for building the EXE file)  
- Pygame (for playing the audio files)  

Once you've installed Python, you can run the following command to automatically download the external packages (you'll need to make sure Python has been added to your system's environment/PATH variables to do this):

``python -m pip install -r requirements.txt``

To build the program, run either `setup.py` (using *_cx_Freeze*) or `py2exe.bat` (using _py2exe_). Both should create a "build" folder containing a "exe.win32-[python version number]" folder that contains the EXE file and relevant libraries.  
As of now, you will (most likely) have to copy all the XML, OGG, PNG, TXT (except requirements.txt) and DB files from the main directory to the build directory where the EXE file is, in order for it to work properly. Currently, the compilation process results in a total file size of over 100MB so, in the future, there may be updates to the build files to reduce the size this program takes up in its compiled state. Also, in the future, there may be the creation of an installer for this program, so do stay tuned!

If you don't want to buld the program and want to run it directly through Python instead, just run `runscript.py` and everything should work fine!

### License

MIT (see LICENSE.txt)