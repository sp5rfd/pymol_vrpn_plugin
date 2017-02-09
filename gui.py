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
mappingFile=0
templateFile=0
structurePdb=0

def chooseTemplateFile():
    global templateFile
    templateFile.set(askopenfilename())
    print "abc"

def chooseMappingFile():
    global mappingFile
    mappingFile.set(askopenfilename())
    print "def"

def run(): 
    print "ruszaj!"

def stop():
    print "stój!"

def statsWindow():
    currentWindow = Tk()
    currentWindow.title("PyMOL VRPN Plugin v1.0")
    currentWindow.geometry("370x280+200+100")
    currentWindow.resizable(False, False)
    currentWindow.call('wm', 'attributes', '.', '-topmost', '1')
    
    vrpnGroup = LabelFrame(currentWindow, text=" VRPN CFG. ", width=350, height=90)
    vrpnGroup.grid(row=0, padx=10, pady=10)
    vrpnGroup.grid_propagate(False)

    Label(vrpnGroup, text="PHANTOM URL: ").grid(row=0, padx=10, pady=10)
    global startButton, stopButton, urlEntry
    urlEntry=Entry(vrpnGroup, width=25, justify=CENTER)
    urlEntry.insert(0,"PHANTOM_URL")
    urlEntry.grid(row=0, column=1, columnspan=2)
    startButton=Button(vrpnGroup, text="START", command=run)
    startButton.grid(row=1, column=1, columnspan=2, sticky=W)
    stopButton=Button(vrpnGroup, text="STOP", command=stop, state=DISABLED)
    stopButton.grid(row=1, column=1, columnspan=2, sticky=E)
    
    atomGroup = LabelFrame(currentWindow, text=" ATOM INFO ", width=350, height=150)
    atomGroup.grid(row=1, padx=10, pady=10)
    atomGroup.grid_propagate(False)
    Label(atomGroup, text="Symbol chemiczny:").grid(row=0, padx=10, pady=5)
    global atomSymbol, atomX, atomY, atomZ
    atomSymbol=Entry(atomGroup, width=15, justify=CENTER)
    atomSymbol.grid(row=0, column=1)
    Label(atomGroup, text="Pozycja X=").grid(row=1, sticky=E, padx=10, pady=5)
    atomX=Entry(atomGroup, width=15, justify=CENTER)
    atomX.grid(row=1, column=1)
    Label(atomGroup, text="Pozycja Y=").grid(row=2, sticky=E, padx=10, pady=5)
    atomY=Entry(atomGroup, width=15, justify=CENTER)
    atomY.grid(row=2, column=1)
    Label(atomGroup, text="Pozycja Z=").grid(row=3, sticky=E, padx=10, pady=5)
    atomZ=Entry(atomGroup, width=15, justify=CENTER)
    atomZ.grid(row=3, column=1)
    
    currentWindow.mainloop()

def openStatsWindow():
    global currentWindow
    currentWindow.destroy()
    statsWindow()

def filesWindow():
    global currentWindow,templateFile,mappingFile
    
    currentWindow = Tk()
    currentWindow.call('wm', 'attributes', '.', '-topmost', '1')
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
    
    
    #    ustawianie adresu IP serwera VRPN
    group=LabelFrame(currentWindow,text="Adres IP serwera VRPN",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    vrpnIp=Entry(group,justify=CENTER)
    vrpnIp.insert(0,"127.0.0.1")
    vrpnIp.pack(pady=5,side=LEFT)
    
    group=Frame(currentWindow)
    group.pack(padx=5,expand=TRUE)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    
    closeButton=Button(group,text="Anuluj",command=currentWindow.destroy)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=openStatsWindow)
    nextButton.pack()
    
    currentWindow.mainloop();
    
def openFilesWindow():
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
    
    closeButton=Button(group,text="Anuluj",command=currentWindow.destroy)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=openFilesWindow)
    nextButton.pack()
    
    currentWindow.mainloop();

if __name__ == "__main__":
    startWindow()


