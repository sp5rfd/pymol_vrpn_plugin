import sys
sys.path.append("C:\usr\local\lib\pythondist-packages")
from trace import threading
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
import vrpn_Tracker
import vrpn_Button

x = y = z = dx = dy = dz = 0 #wspolrzedne x,y,z i zmiany tych wspolrzednych
xangle = yangle = zangle = dxangle = dyangle = dzangle = 0  # zmiana wspolrzednych (roznica miedzy wartoscia w kroku n0 i n1)
scale = 100

def buildPlugin():
    gui = GUI()
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: buildPlugin())

#   Klasa VRPNClient jest odpowiedzialna za polaczenie z serwerem VRPN
def handle_tracker(userdata, t):
    global x, y, z, dx, dy, dz
    dx = x-t[1]*scale
    dy = y-t[2]*scale
    dz = z-t[3]*scale
    x = t[1]*scale
    y = t[2]*scale
    z = t[3]*scale
    cmd.translate([-dx, -dy, -dz], object="arrow")
    
    global xangle, yangle, zangle, dxangle, dyangle, dzangle
    dxangle = xangle-t[4]
    dyangle = yangle-t[5]
    dzangle = zangle-t[6]
    xangle = t[4]
    yangle = t[5]
    zangle = t[6]
    cmd.rotate('x', -dxangle*100, object="arrow")
    cmd.rotate('y', -dyangle*100, object="arrow")
    cmd.rotate('z', -dzangle*100, object="arrow")
    
#    print dxangle, dyangle, dzangle
#    sleep(0.1)
    
def handle_button(userdata, b):
    button = b[0]
    status = b[1]
    
    if(button == 0 and status == 1):
        print "rysuje strzalkie"
        doDrawPointer()
        
    if(button == 1 and status == 1):
        print "przekrecam strzalke"
        cmd.rotate('x', 1, object="arrow")
            
def doDrawPointer():
    cone = [
        CONE, 0, 0, 0, 1, 1, 1, #x1, y1, z1, x2, y2, z2
        0.0, 0.1,               # Radius 1, 2
        0.0, 0.0, 0.0,          # RGB Color 1
        5.0, 6.0, 7.0,          # RGB Color 2
        1.0, 1.0]               # Caps 1 & 2
        
    cmd.load_cgo(cone, "arrow")
    
class VRPNClient(Thread):
    tracker = vrpn_Tracker.vrpn_Tracker_Remote("phantom0@localhost")
    button = vrpn_Button.vrpn_Button_Remote("phantom0@localhost")
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        vrpn_Tracker.register_tracker_change_handler(handle_tracker)
        vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(self.tracker, None, vrpn_Tracker.get_tracker_change_handler())
        
        vrpn_Button.register_button_change_handler(handle_button)
        vrpn_Button.vrpn_Button_Remote.register_change_handler(self.button, None, vrpn_Button.get_button_change_handler())
            
    def run(self):
        while 1:
            self.tracker.mainloop()
            self.button.mainloop()
    
    
#   Klasa GUI jest odpowiedzialna za tworzenie 
#   graficznego interfejsu uzytkownika
#   obsluguje take wszystkie zdarzenia
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
        self.buttonsRow = Frame(self.firstTab)
        self.buttonsRow.pack(fill=X, side=TOP)
        self.exitButton = Button(self.buttonsRow, text = "Exit")
        self.exitButton.bind("<Button-1>", self.doExit)
        self.exitButton.pack(side=LEFT)
        
    def doRunVRPN(self, event=None):
        doDrawPointer()
        client = VRPNClient()
        client.start()
        
    def doDrawAxes(self):
        w = 0.06 # cylinder width
        l = 0.75 # cylinder length
        h = 0.25 # cone hight
        d = w * 1.618 # cone base diameter
        
        axes = [
            CYLINDER, 0.0, 0.0, 0.0, l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            CYLINDER, 0.0, 0.0, 0.0, 0.0, l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            CYLINDER, 0.0, 0.0, 0.0, 0.0, 0.0, l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
            CONE, l, 0.0, 0.0, (h+l), 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
            CONE, 0.0, l, 0.0, 0.0, (h+l), 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            CONE, 0.0, 0.0, l, 0.0, 0.0, (h+l), d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
        
        cmd.load_cgo(axes, self.AXES)
        
    def doExit(self):
        print "exit..."
