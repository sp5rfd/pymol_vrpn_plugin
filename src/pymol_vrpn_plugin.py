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
    gui = GUI()
    
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: buildPlugin())

def quaternion2euler(quat_x, quat_y, quat_z, quat_w):
    result = []
    sinThetaOver25q = 1 - quat_w*quat_w
    if(sinThetaOver25q <= 0):
        result[0] = result[1] = result[2] = 0
        return result
    
    oneOverSinThetaOver2 = 1.0/sqrt(sinThetaOver25q)
    result[0] = quat_x*oneOverSinThetaOver2
    result[1] = quat_y*oneOverSinThetaOver2
    result[2] = quat_z*oneOverSinThetaOver2
    return result

def quatconj( Q ):
    return [-Q[0],-Q[1],-Q[2],Q[3]]
 
def quatmag( Q ):
    s = 0.0
    QC = quatconj(Q)
    for x in range(4):
        s += Q[x]*Q[x]
    print s
    return sqrt(s)

def quatnorm( Q ):
    m = quatmag( Q )
    return [q/m for q in Q]

def quat2axisangle( Q ):
    #returns list where 0..2 are rot axis and 3 is angle
    qn = quatnorm( Q )
    cos_a = Q[3]
    angle = acos( cos_a ) * 2
    sin_a = sqrt( 1.0 - cos_a * cos_a )
    if fabs( sin_a ) < 0.000005:
        sin_a = 1
    ax_an = [ q/sin_a for q in Q[0:3] ]
    ax_an.append( angle )
    return ax_an

def quat_to_angle(quat_x, quat_y, quat_z, quat_w):
    print "todo"

#   Klasa VRPNClient jest odpowiedzialna za polaczenie z serwerem VRPN
def handle_tracker(userdata, t):
#    global x0, y0, z0
#    if x0 is None and y0 is None and z0 is None:
    print "wszystko to nic"
    x0 = t[1]
    y0 = t[2]
    z0 = t[3]
        
#    translacje
    global x, y, z, dx, dy, dz
    
    dx = x-t[1]*scale
    dy = y-t[2]*scale
    dz = z-t[3]*scale
    x = x0*scale
    y = y0*scale
    z = z0*scale
    cmd.translate([-dx, -dy, -dz], object="arrow")
    
    GUI.xCoord.delete(0, END)
    GUI.xCoord.insert(0, z)

#    rotacje
    global ex, ey, ez, dex, dey, dez
#   axis_ang = quat_to_angle(t[4], t[5], t[6], t[7])
    
    axis_ang = quat2axisangle([t[4], t[5], t[6], t[7]])   # przeliczenie kwaternionow na "obroty Eulera"
    
    dex = ex-axis_ang[0]
    dey = ey-axis_ang[1]
    dez = ez-axis_ang[2]
    
    ex = axis_ang[0]
    ey = axis_ang[1]
    ez = axis_ang[2]
    
    print "zmiany katow:", dex, dey, dez
    
def handle_button(userdata, b):
    button = b[0]
    status = b[1]
    if(button == 0 and status == 1):
        cmd.rotate('x', -3, object="arrow")
        cmd.rotate('y', -2, object="arrow")
        cmd.rotate('z', -1, object="arrow")
    if(button == 1 and status == 1):
        print "przycisk drugi"
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
        self.geometry("640x480")
        self.title("VRPN Plugin")           #sets window title
        
        Label(self, text="Wspolrzedna X:").grid(row=0)
        Label(self, text="Wspolrzedna Y:").grid(row=1)
        Label(self, text="Wspolrzedna Z:").grid(row=2)
        
        xCoord = Entry(self).grid(row=0, column=1)
        yCoord = Entry(self).grid(row=1, column=1)
        zCoord = Entry(self).grid(row=2, column=1)
        
        runVRPN = Button(self, text="Run VRPN").grid(row=3, column=0)
        runVRPN.bind("<Button-1>", self.doRunVRPN)
        
        testButton = Button(self, text="TEST").grid(row=3, column=1)
        testButton.bind("<Button-1>", self.doTest)
        
        self.mainloop()
        
    def doRunVRPN(self, event=None):
        client = VRPNClient()
        client.start()
        
    def doTest(self):
        print "exit..."
