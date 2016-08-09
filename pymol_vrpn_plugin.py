from math import pi
from math import *
import sys
sys.path.append("/home/crooveck/workspace/pymol_vrpn_plugin/python_vrpn")
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
import vrpn_ForceDevice
from math import *
sys.path.append(".")
from transformations import *

scale = 30
x = y = z = dx = dy = dz = 0 #wspolrzedne x,y,z i zmiany tych wspolrzednych
xStart = yStart = zStart = 0
previous_orientation = 0
rot_angle = rot_x = rot_y = rot_z = drot_angle = drot_x = drot_y = drot_z = 0

def buildPlugin():
    print "ZBUDOWlem PLUGIN VRPN"
    global gui
    gui = GUI()
    gui.mainloop()
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: buildPlugin())

#   Klasa VRPNClient jest odpowiedzialna za polaczenie z serwerem VRPN
def handle_tracker(userdata, t):
#   TRANSLACJE:
#   przesuniecia sa obliczane jako roznica pozycji biezacej i poprzedniej
    global x, y, z, dx, dy, dz, xStart, yStart, zStart

    if(xStart == 0 and yStart == 0 and zStart == 0): 
        xStart = t[1]*scale
        yStart = t[2]*scale
        zStart = t[3]*scale
    
    x0 = t[1]*scale - xStart
    y0 = t[2]*scale - yStart
    z0 = t[3]*scale - zStart
    
    dx = x-x0   
    dy = y-y0   
    dz = z-z0   
#   funkcja dokonujaca przeksztalcenia - transjacji
    cmd.translate(vector=[-dx,-dy,-dz],object="arrow",camera=0)
    
    x = x0
    y = y0
    z = z0
    
#   ROTACJE
    global previous_orientation
    # bierzacy stan - orientacja
    current_orientation=(t[5],t[6],t[7],t[4])   # inny format kwaterniona do transformations.py niz dostaje z VRPN
    # przy pierwszym uruchomieniu 
    # gdy nie ma poprzedniej orientacji 
    if(previous_orientation == 0):
        previous_orientation=current_orientation
    
    rotation_quaternion=quaternion_multiply(quaternion_inverse(current_orientation),previous_orientation)
    
    # konczymy robote wiec musze zapamietac bierzaca 
    # obecna orientacje. Dalej bedzie ona juz poprzenia.
    previous_orientation=current_orientation
    
    rotation_matrix = quaternion_matrix(rotation_quaternion) # Return homogeneous rotation matrix from quaternion.
    (rotation_angle,rotation_axis,point) = rotation_from_matrix(rotation_matrix)

#    print rotation_axis
    cmd.rotate(axis=[rotation_axis[0],rotation_axis[1],rotation_axis[2]], 
            angle=(rotation_angle*180/math.pi), origin=[x,y,z], object="arrow", camera=0)


def handle_button(userdata, b):
    button = b[0]
    status = b[1]
    
    if(button == 0 and status == 1):    # wcisnieto przycisk pierwszy
        print "wcisnieto przycisk pierwszy"  
        cmd.rotate('x', -3, object="arrow")
        cmd.rotate('y', -2, object="arrow")
        cmd.rotate('z', -1, object="arrow")
    if(button == 1 and status == 1):    # wcisnieto przycisk drugi
        print "wcisnieto przycisk drugi"
        cmd.rotate('x', 3, object="arrow")
        cmd.rotate('y', 2, object="arrow")
        cmd.rotate('z', 1, object="arrow")
        
def force_handler(userdata, t):
    s="lala"
#    print "sila",t,userdata
        
            
def doDrawPointer(x0, y0, z0):    
    cone = [
        CONE, 0, 0, 0, 0, 0, 1, #x1, y1, z1, x2, y2, z2
        0.0, 0.3,               # Radius 1, 2
        1,0,1,          # RGB Color 1
        1,1,0,            # RGB Color 2
        1.0,1.0]               # Caps 1 & 2
        
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
        
class VRPNClient(threading.Thread):
    PHANTOM_URL = "phantom0@172.21.5.156"
    tracker = vrpn_Tracker.vrpn_Tracker_Remote(PHANTOM_URL)
    button = vrpn_Button.vrpn_Button_Remote(PHANTOM_URL)
    forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(PHANTOM_URL)
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        vrpn_Tracker.register_tracker_change_handler(handle_tracker)
        vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(self.tracker, None, vrpn_Tracker.get_tracker_change_handler())
        
        vrpn_Button.register_button_change_handler(handle_button)
        vrpn_Button.vrpn_Button_Remote.register_change_handler(self.button, None, vrpn_Button.get_button_change_handler())
            
        vrpn_ForceDevice.register_force_change_handler(force_handler)
        vrpn_ForceDevice.vrpn_ForceDevice_Remote.register_force_change_handler(self.forceDevice, None, vrpn_ForceDevice.get_force_change_handler())
            
    def run(self):
        doDrawPointer(0, 0, 0)
        doDrawAxes(0, 0, 0)
        sleep(1)
        
        while True:
            self.tracker.mainloop()
            self.button.mainloop()
            self.forceDevice.mainloop()
    
    
#   Klasa GUI jest odpowiedzialna za tworzenie 
#   graficznego interfejsu uzytkownika
#   obsluguje take wszystkie zdarzenia
class GUI(Tk):
    AXES = 'axes'
    ARROW = 'arrow'
    
    def __init__(self):
        Tk.__init__(self)
        self.geometry("420x240")
        self.title("VRPN Plugin")           #sets window title
        
        Label(self, text="Wspolrzedna X:").grid(row=0)
        Label(self, text="Wspolrzedna Y:").grid(row=1)
        Label(self, text="Wspolrzedna Z:").grid(row=2)
        
        xEntry = Entry(self)
        xEntry.grid(row=0, column=1)
        
        yEntry = Entry(self)
        yEntry.grid(row=1, column=1)
        
        zEntry = Entry(self)
        zEntry.grid(row=2, column=1)
        
        Button(self, text="START", command=self.doRunVRPN).grid(row=0, column=3)
        Button(self, text="STOP", command=self.doStop).grid(row=1, column=3)
        
    def doRunVRPN(self, event=None):
        self.client = VRPNClient()
        self.client.start()
        
    def doStop(self, event=None):
        print "TODO: zatrzymywanie"
