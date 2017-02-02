#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from Tkinter import *
from tkFileDialog import *

helloMsg="\
Witaj użytkowniku.\
\nW tej aplikacji masz możliwość dopasowania lokalnie optymalnych struktur\
\ncząsteczek chemicznych takich jak białka czy kwasy nukleinowe\
\nlklklk"

currentWindow=0
mappingFile=""
templateFile=""
structurePdb=0

def chooseTemplateFile():
    global templateFile
    templateFile.set(askopenfilename())

def chooseMappingFile():
    global mappingFile
    mappingFile.set(askopenfilename())

def filesWindow():
    global currentWindow,templateFile,mappingFile
    
    currentWindow = Tk()
    currentWindow.title("Eksplorator lokalnych podobieństw struktur przestrzennych")

    templateFile=StringVar(value=os.getcwd()+"/")
    mappingFile=StringVar(value=os.getcwd()+"/")
    
    w=640
    h=480
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
    group=LabelFrame(currentWindow,text="Wzorzec",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    message="Wzorzec jest strukturą, którą będziemy próbowali dopasować do cząsteczki bazowej.\
    \nWzorzec może stanowić wycinek cząsteczki bazowej, np. jakaś struktura drugorzędowa"
    
    label=Label(group,text=message,bg="green",anchor=W)
    label.pack(fill=BOTH)
    
    fileName=Entry(group,textvariable=templateFile,width=50,state="readonly")
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik",command=chooseTemplateFile)
    fileChooser.pack(side=LEFT)
    
    group=LabelFrame(currentWindow,text="Plik mapowania",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    label=Label(group,text="Tutaj wybierz plik mapowania",bg="green",anchor=W)
    label.pack(fill=BOTH)
    
    fileName=Entry(group,textvariable=mappingFile,width=50,state="readonly")
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik",command=chooseMappingFile)
    fileChooser.pack(side=LEFT)
    
    group=LabelFrame(currentWindow,text="Identyfikator PDB",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    label=Label(group,text="Tutaj wybierz plik ",bg="green",anchor=W)
    label.pack(fill=BOTH)
        
    fileName=Entry(group)
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik")
    fileChooser.pack(side=LEFT)
    
    group=Frame(currentWindow)
    group.pack(padx=5,expand=TRUE)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    
    closeButton=Button(group,text="Anuluj",command=sys.exit)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej")
    nextButton.pack()
    
    currentWindow.mainloop();
    
def nextWindow():
    global currentWindow
    currentWindow.destroy()
    filesWindow()
    
def startWindow():
    global currentWindow
    currentWindow = Tk()
    currentWindow.title("Eksplorator lokalnych podobieństw struktur przestrzennych")

    w=640
    h=480
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
    group=LabelFrame(currentWindow,text="Witaj",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5,expand=True)
    
    label=Label(group,text=helloMsg,bg="green")
    label.pack(fill=BOTH,side=LEFT)
    
    dnaImage=PhotoImage(file="dna.gif")
    
    label=Label(group,image=dnaImage)
    label.pack(fill=BOTH)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    
    closeButton=Button(group,text="Anuluj",command=sys.exit)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=nextWindow)
    nextButton.pack()
    
    currentWindow.mainloop();

if __name__ == "__main__":
    startWindow()


