from cx_Freeze import setup, Executable
import sys

sys.argv.append("build")

xtarg = Executable(
    script = "runscript.py",
    base = "Win32GUI",
    targetName = "AC Soft Skill Assessment Program.exe",
    icon = "aclogo.ico"
    )

setup(
    name = "AC Soft Skills Assessment Program",
    version = "0.1",
    description = "My NEA Coursework Program (AQA), a program for assessing a SEN student's soft skills in an electronic and archivable manner.",
    author = "Zishan Rahman",
    executables = [xtarg]
    )
