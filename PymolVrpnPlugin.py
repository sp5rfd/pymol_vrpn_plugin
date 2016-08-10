"""
    This program was created in 2015-16 by Pawel Tomaszewski
    In cooperation with Biophysics Laboratory of Warsaw University
"""

import sys
sys.path.append("/home/crooveck/workspace/pymol_vrpn_plugin/python_vrpn")
sys.path.append(".")
from transformations import *
from Tkinter import *
from ttk import *
from pymol import *
from pymol.cgo import *
from time import *
import vrpn_Tracker
import vrpn_Button
import vrpn_ForceDevice
from math import *

"""
    Mainloop running flag. This indicates if threads and mainloops are running.
"""
IS_RUNNING = False

"""
    Phantom VRPN URL.
"""
PHANTOM_URL = "phantom0@172.21.5.156"

"""
    Global variables for translations. 
    trackerX,trackerY,trackerZ - Phantom native coordinates
    x,y,z - Pymol coordinates
    scale - ratio between PYMOL and PHANTOM coordinate
"""
trackerX = trackerY = trackerZ = 0
x = y = z = 0 
scale=750

"""
    Global variables for rotations
    previous_orientation stores a quaternion that represent previous orientation
"""
previous_orientation=0

def tracker_handler(u, tracker):
    global trackerX, trackerY, trackerZ
    trackerX = tracker[1]
    trackerY = tracker[2]
    trackerZ = tracker[3]
    
#   TRANSLACJE:
    x0 = trackerX*scale
    y0 = trackerY*scale
    z0 = trackerZ*scale
#   funkcja dokonujaca przeksztalcenia - transjacji
    global x, y, z
    cmd.translate(vector=[(x0-x), (y0-y), (z0-z)], object="arrow", camera=0)
    x = x0
    y = y0
    z = z0
    
#   ROTACJE
    global previous_orientation
    # bierzacy stan - orientacja
    orientation=(tracker[5],tracker[6],tracker[7],tracker[4])   # inny format kwaterniona do transformations.py niz dostaje z VRPN
    # przy pierwszym uruchomieniu 
    # gdy nie ma poprzedniej orientacji 
    if(previous_orientation == 0):
        previous_orientation=orientation
    
    rotation_quaternion=quaternion_multiply(quaternion_inverse(orientation),previous_orientation)
    previous_orientation=orientation
    
    rotation_matrix = quaternion_matrix(rotation_quaternion) # Return homogeneous rotation matrix from quaternion.
    (rotation_angle,rotation_axis,point) = rotation_from_matrix(rotation_matrix)

    cmd.rotate(axis=[rotation_axis[0],rotation_axis[1],rotation_axis[2]], 
            angle=(rotation_angle*180/math.pi), origin=[x,y,z], object="arrow", camera=0)


def button_handler(u, button):
    status = button[1]
    
    msg = ""
    if(status):
        msg += "Wcisnieto "
    else:
        msg += "Puszczono "
        
    msg += "przycisk "
    
    if(button[0]):
        msg += "gorny."
    else:
        msg += "dolny."
    
    print msg
    
def force_handler(u, force):
#    print "force",force
    abc='test'
    
def draw_pointer():
    pointer = [
        CONE, 0,0,0, 0,0,10,   #x1, y1, z1, x2, y2, z2
        0.0, 1,                                   # Radius 1, 2
        1, 0, 1,                                    # RGB Color 1
        1, 1, 0,                                    # RGB Color 2
        1.0, 1.0 ]                                  # Caps 1 & 2
        
    cmd.load_cgo(pointer, "arrow")
    
def draw_axes(x0, y0, z0):
    w = 0.5 # cylinder width
    l = 10 # cylinder length
    h = 2 # cone hight
    d = w * 1.618 # cone base diameter
    
    axes = [
        CYLINDER, x0, y0, z0, l, 0.0, 0.0, w, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
        CYLINDER, x0, y0, z0, 0.0, l, 0.0, w, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
        CYLINDER, x0, y0, z0, 0.0, 0.0, l, w, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
        CONE, l, 0.0, 0.0, (h+l), 0.0, 0.0, d, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,
        CONE, 0.0, l, 0.0, 0.0, (h+l), 0.0, d, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
        CONE, 0.0, 0.0, l, 0.0, 0.0, (h+l), d, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0]

    cmd.load_cgo(axes, "axes")

def find_closest(x0,y0,z0):
    stored.pos = []                                                                                                                
    cmd.iterate_state(1, 'all', 'stored.pos.append((x,y,z))')
    
    minDistance=sys.float_info.max     # poczatkowa wartosc minimalna powinna byc duza
    minNumber=0                     # index najmniejszej wartosci
    # liczymy najblizszy atom 
    for atomNumber in xrange(0,len(stored.pos)):
        xDistance = stored.pos[atomNumber][0]-x0
        yDistance = stored.pos[atomNumber][1]-y0
        zDistance = stored.pos[atomNumber][2]-z0
        distance=sqrt(math.pow(xDistance,2)+math.pow(yDistance,2)+math.pow(zDistance,2))
        
        if(distance<minDistance):
            minDistance=distance
            minNumber=atomNumber
    
    return (stored.pos[minNumber][0]/scale, stored.pos[minNumber][1]/scale, stored.pos[minNumber][2]/scale)
    
    
def vrpn_client():
    print "Starting VRPN client..."
    
    tracker = vrpn_Tracker.vrpn_Tracker_Remote(PHANTOM_URL)
    vrpn_Tracker.register_tracker_change_handler(tracker_handler)
    vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker, None, vrpn_Tracker.get_tracker_change_handler())

    button = vrpn_Button.vrpn_Button_Remote(PHANTOM_URL)
    vrpn_Button.register_button_change_handler(button_handler)
    vrpn_Button.vrpn_Button_Remote.register_change_handler(button, None, vrpn_Button.get_button_change_handler())

    forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(PHANTOM_URL)
    vrpn_ForceDevice.register_force_change_handler(force_handler)
    vrpn_ForceDevice.vrpn_ForceDevice_Remote.register_force_change_handler(forceDevice, None, vrpn_ForceDevice.get_force_change_handler())
    
    draw_axes(0,0,0)
    draw_pointer()
    sleep(1)
    
    while IS_RUNNING:
        tracker.mainloop()
        button.mainloop()
        forceDevice.mainloop()
        
        if True:
            # znajduje najblizszy punkt do aktualnej pozycji wskaxnika PyMol
            point = find_closest(x,y,z)
            
            force=100   # wielkosc sily |F|
            forceX = (point[0]-trackerX)    # wektor sily X
            forceY = (point[1]-trackerY)    # j.w. Y
            forceZ = (point[2]-trackerZ)    # j.w. Z
                
            forceDevice.setFF_Origin(trackerX, trackerY, trackerZ)
            forceDevice.setFF_Force(force*forceX, force*forceY, force*forceZ)
            forceDevice.setFF_Jacobian(force,0,0, 0,force,0, 0,0,force)
            forceDevice.setFF_Radius(0.1)
            forceDevice.sendForceField()

    print "Finishing work..."

def run():
    global IS_RUNNING
    IS_RUNNING = True
    
    thread.start_new_thread(vrpn_client, ())
    
    # listuje wspolrzedne atomow
#    stored.pos = [] 
#    cmd.iterate_state(1, 'all', 'stored.pos.append((x,y,z))')
#    
#    for pos in stored.pos:
#        print pos[0],pos[1],pos[2]

    
def stop():
    global IS_RUNNING
    IS_RUNNING = False
    
def build_gui():
    window = Tk()
    window.title("PyMol VRPN Plugin v1.0")
    window.geometry("200x200")
    
    startButton = Button(window, text="START", command=run).grid(row=0, column=0)
    stopButton = Button(window, text="STOP", command=stop).grid(row=0, column=1)
    
    window.mainloop()
    
def __init__(self):
    print "__init__"
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: build_gui())
                             