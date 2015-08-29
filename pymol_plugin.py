from math import pi
from math import *
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
from math import *
sys.path.append(".")
from transformations import *

scale = 30
x = y = z = dx = dy = dz = 0 #wspolrzedne x,y,z i zmiany tych wspolrzednych
xStart = yStart = zStart = 0

rot_angle = rot_x = rot_y = rot_z = drot_angle = drot_x = drot_y = drot_z = 0

def buildPlugin():
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
        print "pozycja startowa: ", xStart, yStart, zStart
    
    x0 = t[1]*scale - xStart
    y0 = t[2]*scale - yStart
    z0 = t[3]*scale - zStart
    
    dx = x-x0   
    dy = y-y0   
    dz = z-z0   
#   funkcja dokonujaca przeksztalcenia - transjacji
    cmd.translate(vector=[-dz, -dy, dx], object="arrow", camera=1)
    
    x = x0
    y = y0
    z = z0
    
#   ROTACJE
    
    global rot_angle, rot_x, rot_y, rot_z, drot_angle, drot_x, drot_y, drot_z
#    cmd.rotate(axis="y", angle=1, origin=[x,y,z], object="arrow", camera=1)
#    cmd.rotate(axis=[x,y,z], angle=1, origin=[x,y,z], object="arrow", camera=1)
    
    m = quaternion_matrix([t[4], t[5], t[6], t[7]]) #sdfs
    M = [m[0,0], m[0,1], m[0,2], m[0,3], m[1,0], m[1,1], m[1,2], m[1,3], m[2,0], m[2,1], m[2,2], m[2,3], m[3,0], m[3,1], m[3,2], m[3,3]]
    cmd.transform_selection(selection="all", matrix=M, homogenous=0)
    print M
    
#    rot_angle0 = 2*acos(qw)
#    rot_x0 = qx/sqrt(1-qw*qw)
#    rot_y0 = qy/sqrt(1-qw*qw)
#    rot_z0 = qz/sqrt(1-qw*qw)
    
#    drot_angle = rot_angle-rot_angle0
#    drot_x = rot_x-rot_x0
#    drot_y = rot_y-rot_y0
#    drot_z = rot_z-rot_z0
    
     
#    cmd.rotate(axis=[1,0,0], angle=drot_angle*scale, origin=[x,y,z], object="arrow", camera=0)
#    cmd.rotate(axis=[rot_x,rot_y,rot_z], angle=rot_angle, origin=[x,y,z], object="arrow", camera=1)
#    
#    rot_angle = rot_angle0
#    rot_x = rot_x0
#    rot_y = rot_y0
#    rot_z = rot_z0
    
def handle_button(userdata, b):
    print "wcisnieto przycisk"
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
        doDrawPointer(0, 0, 0)
        doDrawAxes(0, 0, 0)
        
    def doStop(self, event=None):
        print "TODO: zatrzymywanie"
