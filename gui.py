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
    global currentWindow,IS_RUNNING
    
    IS_RUNNING = True
#    thread.start_new_thread(vrpn_client, ())
    
    currentWindow.destroy()
    
    w=640
    h=480
    currentWindow=Tk()
    currentWindow.title("Eksplorator lokalnych podobieństw struktur przestrzennych")
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    currentWindow.attributes('-topmost', 1)
    currentWindow.resizable(False, False)
    currentWindow.grid_columnconfigure(0, weight=1)
    currentWindow.grid_columnconfigure(1, weight=1)
    
    global atomSymbol, atomX, atomY, atomZ
    group=LabelFrame(currentWindow, text="ATOM INFO")
    group.grid(column=0,padx=5,pady=5,sticky='WE')
    Label(group, text="Symbol chemiczny:",bg="green").grid(row=0)
    Entry(group, width=15, justify=CENTER).grid(row=1)
    Label(group, text="Pozycja X=",bg="green",anchor=W).grid(row=2,sticky='WE')
    atomX=Entry(group, width=15, justify=CENTER)
    atomX.grid(row=3)
    Label(group, text="Pozycja Y=",bg="green",anchor=W).grid(row=4,sticky='WE')
    atomY=Entry(group, width=15, justify=CENTER)
    atomY.grid(row=5)
    Label(group, text="Pozycja Z=",bg="green",anchor=W).grid(row=6,sticky='WE')
    atomZ=Entry(group, width=15, justify=CENTER)
    atomZ.grid(row=7)
    
    global forceType
    forceType=IntVar()
    forceType.set(1)
    group=LabelFrame(currentWindow,text="Typ siły")
    group.grid(column=1,row=0,sticky='NSWE',pady=5,padx=5)
    Radiobutton(group,text="Force Field",variable=forceType,value=0).grid(row=0,sticky="W")
    Radiobutton(group,text="lala",variable=forceType,value=1).grid(row=1,sticky="W")
    Radiobutton(group,text="blabla",variable=forceType,value=2).grid(row=2,sticky="W")
    
#    spacer
#    Frame(currentWindow).pack(padx=5,expand=TRUE)
    Frame(currentWindow).grid(sticky='NS')
    
#    przycisk stop
    group=Frame(currentWindow)
#    group.pack(padx=5,pady=5)
    group.grid()
    stopButton=Button(group, text="STOP", command=stop)
#    stopButton.pack()
    stopButton.grid()
    
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
    
    message="Wzorzec jest strukturą, którą będziemy próbowali dopasować do cząsteczki bazowej.\
    \nWzorzec może stanowić wycinek cząsteczki bazowej, np. jakaś struktura drugorzędowa"
    
    group=LabelFrame(currentWindow,text="Wzorzec",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
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
    nextButton=Button(group,text="Dalej",command=statsWindow)
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


