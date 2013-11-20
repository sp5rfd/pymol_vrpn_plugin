
#from trace import threading
from threading import Thread
from multiprocessing import Process
import os
import Tkinter 
import tkMessageBox
from Tkinter import *
import ttk
from ttk import *
import pymol
from pymol import *
from pymol.cgo import *
from time import *
#
import vrpn_Tracker
import vrpn_Button

def buildPlugin():
#    gui = GUI()
    print "elo"
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: buildPlugin())

#   Klasa VRPNClient jest odpowiedzialna za polaczenie z serwerem VRPN
#   
class VRPNClient(Thread):
    tracker = vrpn_Tracker.vrpn_Tracker_Remote("phantom0@localhost")
    button = vrpn_Button.vrpn_Button_Remote("phantom0@localhost")
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        vrpn_Tracker.register_tracker_change_handler(handle_tracker)
        vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker, None, vrpn_Tracker.get_tracker_change_handler())
        
        vrpn_Button.register_button_change_handler(handle_button)
        vrpn_Button.vrpn_Button_Remote.register_change_handler(button, None, vrpn_Button.get_button_change_handler())
        
        self.start()

    def hangle_tracker(userdata, t):
        print t
        
    def handle_button(userdata, b):
        button_number = b[0]
        status = b[1]
        if(status == 1):
            print "przycisk ", button_number, " zostal wcisniety"
        else:
            print "przycisk ", button_number, " zostal puszczony"    
            
    def run(self):
        while 1:
            print "eloelo"
            tracker.mainloop()
            button.mainloop()
    
    
    
#   Klasa GUI jest odpowiedzialna za tworzenie 
#   graficznego interfejsu uzytkownika
#   obsluguje tak¿e wszystkie zdarzenia
class GUI(Tk):
    AXES = 'axes'
    ARROW = 'arrow'
    
    def __init__(self):
        Tk.__init__(self)
        self.geometry('300x150')
        self.title("VRPN Plugin")           #sets window title
        
        self.tabs = Notebook(self)
        
        self.firstTab = Frame(self.tabs)
        self.tabs.add(self.firstTab, text = 'First tab')
        self.buildFirstTab()                # builds stuff for first tab
        
        self.secondTab = Frame(self.tabs)
        self.tabs.add(self.secondTab, text = 'Second tab')
        self.buildSecondTab()
        
        self.thirdTab = Frame(self.tabs)
        self.tabs.add(self.thirdTab, text = 'Third tab')
        self.buildThirdTab()
        self.tabs.pack(fill = BOTH, expand=1)
        self.doDrawAxes()
        
        self.mainloop()
        
    def buildThirdTab(self):
        self.runVRPN = Button(self.thirdTab, text="Run VRPN")
        self.runVRPN.bind("<Button-1>", self.doRunVRPN)
        self.runVRPN.pack()
        
    def buildFirstTab(self):
        self.xRow = Frame(self.firstTab)
        self.xRow.pack(fill=X, side=TOP, padx=10)
        self.xLabel = Label(self.xRow, text = 'X: ')   #creates new label
        self.xLabel.pack(side=LEFT)                    #and packs it
        self.xEntry = Entry(self.xRow)
        self.xEntry.pack(side=LEFT)
        
        self.yRow = Frame(self.firstTab)
        self.yRow.pack(fill=X, side=TOP, padx=10)
        self.yLabel = Label(self.yRow, text = 'Y: ')
        self.yLabel.pack(side=LEFT)
        self.yEntry = Entry(self.yRow)
        self.yEntry.pack(side=LEFT)
         
        self.zRow = Frame(self.firstTab)
        self.zRow.pack(fill=X, side=TOP, padx=10)
        self.zLabel = Label(self.zRow, text = "Z: ")
        self.zLabel.pack(side=LEFT)
        self.zEntry = Entry(self.zRow)
        self.zEntry.pack(side=LEFT)
         
        self.buttonsRow = Frame(self.firstTab)
        self.buttonsRow.pack(fill=X, side=TOP)
        self.drawButton = Button(self.buttonsRow, text = "Draw cone")
        self.drawButton.bind("<Button-1>", self.doDraw)
        self.drawButton.pack(side=LEFT)
        self.exitButton = Button(self.buttonsRow, text = "Exit")
        self.exitButton.bind("<Button-1>", self.doExit)
        self.exitButton.pack(side=LEFT)
        
    def buildSecondTab(self):
        self.stepsEntry = Entry(self.secondTab, text=0)
        self.stepsEntry.pack(side=LEFT)
        
        self.upDownButton = Button(self.secondTab, text="Up/Down")
        self.upDownButton.bind("<Button-1>", self.doMoveUpDown)
        self.upDownButton.pack()
        
        self.backForthButton = Button(self.secondTab, text="Back/Forth")
        self.backForthButton.bind("<Button-1>", self.doMoveBackForth)
        self.backForthButton.pack()
        
        self.leftRightButton = Button(self.secondTab, text="Left/Right")
        self.leftRightButton.bind("<Button-1>", self.doMoveLeftRight)
        self.leftRightButton.pack()
        
    def doMoveLeftRight(self, event=None):
        print "czekamy..."
        sleep(5)
        vec = [self.stepsEntry.get(), 0, 0]
        cmd.translate(vec, object=self.ARROW)
        print "no i poczekalismy"
    
    def doMoveUpDown(self, event=None):
        vec = [0, self.stepsEntry.get(), 0]
        cmd.translate(vec, object=self.ARROW)
        
    def doMoveBackForth(self, step=0):
        vec = [0, 0, self.stepsEntry.get()]
        cmd.translate(vec, object=self.ARROW)
        
    def doRunVRPN(self, event=None):
        print "==============VRPN+++++++++++++++++"
#        vrpn = VRPNClient()
        
    def doDrawAxes(self):
        w = 0.06 # cylinder width
        l = 0.75 # cylinder length
        h = 0.25 # cone hight
        d = w * 1.618 # cone base diameter
        
        axes = [
            CYLINDER, 0.0, 0.0, 0.0, l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            CYLINDER, 0.0, 0.0, 0.0, 0.0, l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            CYLINDER, 0.0, 0.0, 0.0, 0.0, 0.0, l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
            CONE, l, 0.0, 0.0, h+l, 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
            CONE, 0.0, l, 0.0, 0.0, h+l, 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            CONE, 0.0, 0.0, l, 0.0, 0.0, h+l, d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
         
        cmd.load_cgo(axes, self.AXES)
    
    def doDraw(self, event=None):
        x = self.xEntry.get()
        y = self.yEntry.get()
        z = self.zEntry.get()
        
        cone = [
            CONE,
            x, y, z,      # XYZ 1
            int(x)+0.8, int(y)+0.8, int(z)+0.8,  # XYZ 2
            0.0, 0.1, # Radius 1, 2
            0.0, 0.0, 0.0,          # RGB Color 1
            1.0, 1.0, 1.0,          # RGB Color 2
            1.0, 1.0]               # Caps 1 & 2
        
        cmd.load_cgo(cone, self.ARROW)
        
    def doTranslate(self, x = 0, y = 0, z = 0):
        print "moving object by x=", x, ",y=", y, ",z=", z
        vec = [x,y,z]
        cmd.translate(vec, object='strzala')
        
    def doRotate(self, axis, angle):
        print "rotating around axis = ", axis, " angle=", angle
        
    def doExit(self, event = None): 
        print "exit..."
        
        

                             
                             