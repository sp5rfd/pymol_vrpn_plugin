#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *

helloMsg="\
Witaj użytkowniku.\
\nW tej aplikacji masz możliwość dopasowania lokalnie optymalnych struktur\
\ncząsteczek chemicznych takich jak białka czy kwasy nukleinowe\
\nlklklk"

def filesWindow():
    window = Tk()
    window.title("Eksplorator lokalnych podobieństw struktur przestrzennych")

    w=640
    h=480
    x=window.winfo_screenwidth()/2 - w/2
    y=window.winfo_screenheight()/2 - h/2
    window.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
    group=LabelFrame(window,text="Witaj",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5,expand=True)
    
    label=Label(group,text=helloMsg,bg="green")
    label.pack(fill=BOTH,side=LEFT)
    
    dnaImage=PhotoImage(file="dna.gif")
    
    label=Label(group,image=dnaImage)
    label.pack(fill=BOTH)
    
    group=Frame(window)
    group.pack(padx=5)
    
    closeButton=Button(group,text="Anuluj",command=closeAction)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=nextAction)
    nextButton.pack()
    
    window.mainloop();

def closeAction():
    sys.exit()
    
def nextAction(prevWindow):
    prevWindow.close()
    filesWindow()
    
def startWindow():
    window = Tk()
    window.title("Eksplorator lokalnych podobieństw struktur przestrzennych")

    w=640
    h=480
    x=window.winfo_screenwidth()/2 - w/2
    y=window.winfo_screenheight()/2 - h/2
    window.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
    group=LabelFrame(window,text="Witaj",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5,expand=True)
    
    label=Label(group,text=helloMsg,bg="green")
    label.pack(fill=BOTH,side=LEFT)
    
    dnaImage=PhotoImage(file="dna.gif")
    
    label=Label(group,image=dnaImage)
    label.pack(fill=BOTH)
    
    group=Frame(window)
    group.pack(padx=5)
    
    closeButton=Button(group,text="Anuluj",command=closeAction)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=nextAction(window))
    nextButton.pack()

    
    window.mainloop();



if __name__ == "__main__":
    startWindow()


