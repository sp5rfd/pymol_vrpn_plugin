from math import pi
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
from math import *


x = y = z = dx = dy = dz = 0 #wspolrzedne x,y,z i zmiany tych wspolrzednych

ex = ey = ez = dex = dey = dez = 0 # wsp. katowe obrotu wokol danych osi oraz zmiany tych wsp.
xangle = yangle = zangle = dxangle = dyangle = dzangle = 0  # zmiana wspolrzednych (roznica miedzy wartoscia w kroku n0 i n1)
scale = 100

def buildPlugin():
    global gui
    gui = GUI()
    gui.mainloop()
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: buildPlugin())

#   Klasa VRPNClient jest odpowiedzialna za polaczenie z serwerem VRPN
def handle_tracker(userdata, t):
    global x, y, z, dx, dy, dz
    
    x0 = t[1]*scale
    y0 = t[2]*scale
    z0 = t[3]*scale
    
    dx = x-x0
    dy = y-y0
    dz = z-z0
    
    cmd.translate(vector=[-dx, -dy, -dz], object="arrow", camera=0)
    
    x = x0
    y = y0
    z = z0
    cmd.rotate(axis="y", angle=1, origin=[x,y,z], object="arrow", camera=0)
    
#    quaternion = [t[4], t[5], t[6], t[7]]
#    
#    result = euler_from_quaternion(quaternion)
#    print quaternion
#    cmd.rotate(axis="y", angle=1, origin=[result[0],result[1],result[2]], object="arrow", camera=0)
    
def handle_button(userdata, b):
    button = b[0]
    status = b[1]
    
    if(button == 0 and status == 1):    # wcisnieto przycisk pierwszy
        cmd.rotate('x', -3, object="arrow")
        cmd.rotate('y', -2, object="arrow")
        cmd.rotate('z', -1, object="arrow")
    if(button == 1 and status == 1):    # wcisnieto przycisk drugi
        cmd.rotate('x', 3, object="arrow")
        cmd.rotate('y', 2, object="arrow")
        cmd.rotate('z', 1, object="arrow")
        
            
def doDrawPointer(x0, y0, z0):
    cone = [
        CONE, 0, 0, 0, 1, 1, 1, #x1, y1, z1, x2, y2, z2
        0.0, 1.0,               # Radius 1, 2
        0.0, 0.0, 0.0,          # RGB Color 1
        5.0, 6.0, 7.0,          # RGB Color 2
        1.0, 1.0]               # Caps 1 & 2
        
    cmd.load_cgo(cone, "arrow")
    
def doDrawAxes(x0, y0, z0):
        w = 0.06 # cylinder width
        l = 0.75 # cylinder length
        h = 0.25 # cone hight
        d = w * 1.618 # cone base diameter
        axes = [
            CYLINDER, x0, y0, z0, l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            CYLINDER, x0, y0, z0, 0.0, l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            CYLINDER, x0, y0, z0, 0.0, 0.0, l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
            CONE, l, 0.0, 0.0, (h+l), 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
            CONE, 0.0, l, 0.0, 0.0, (h+l), 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            CONE, 0.0, 0.0, l, 0.0, 0.0, (h+l), d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]
        
        cmd.load_cgo(axes, "axes")
        
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
        doDrawPointer(0, 0, 0)
        doDrawAxes(0, 0, 0)
        sleep(1)
        
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
        self.geometry("320x240")
        self.title("VRPN Plugin")           #sets window title
        
        Label(self, text="Wspolrzedna X:").grid(row=0)
        Label(self, text="Wspolrzedna Y:").grid(row=1)
        Label(self, text="Wspolrzedna Z:").grid(row=2)
        
        Entry(self).grid(row=0, column=1)
        Entry(self).grid(row=1, column=1)
        Entry(self).grid(row=2, column=1)
        
        Button(self, text="RUN_VRPN", command=self.doRunVRPN).grid(row=0, column=3)
        Button(self, text="TEST_123", command=self.doTest).grid(row=1, column=3)
        
    def doRunVRPN(self, event=None):
        client = VRPNClient()
        client.start()
        
    def doTest(self, event=None):
        print "test123"