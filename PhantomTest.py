# VRPN
import sys
sys.path.append("/home/crooveck/workspace/vrpn/build_new/python_vrpn")
import vrpn_Tracker
import vrpn_Button
import vrpn_ForceDevice
# transformations
sys.path.append(".")
from transformations import *
# inne
from time import *
from math import *

print "\t+--------------------------------+"
print "\t|   SensAble Phantom Omni Test   |"
print "\t+--------------------------------+"

def quat_to_ogl_matrix(qx,qy,qz,qw):
    print("qx=%f, qy=%f, qz=%f, qw=%f" % (qx,qy,qz,qw))
    return (1,2,3,4,11,22,33,44,111,222,333,444,1111,2222,3333,4444)
    

def button_handler(userdata, b):
    button = b[0]
    state = b[1]
    
    msg = ""
    if(state==1):
        msg += "Wcisnieto "
    else:
        msg += "Puszczono "
        
    msg += "przycisk "
    
    if(button==1):
        msg += "gorny."
    else:
        msg += "dolny."
    
    print msg

def tracker_handler(userdata, tracker):
    global previous_orientation, position
    
    position=(tracker[1],tracker[2],tracker[3])
    current_orientation=(tracker[5],tracker[6],tracker[7],tracker[4])
    
#    print("\n-------------------")
#    print("POZYCJA: (%f,%f,%f)" % (position[0],position[1],position[2]))

    if(previous_orientation==0): 
        previous_orientation=current_orientation

    print("ORIENTACJA:")
    print("    poprzednia: (%f,%f,%f,%f)" % (previous_orientation[0],previous_orientation[1],previous_orientation[2],previous_orientation[3]))
    print("    obecna: (%f,%f,%f,%f)" % (current_orientation[0],current_orientation[1],current_orientation[2],current_orientation[3]))
    
    # current_orientation=(t[5],t[6],t[7],t[4])   # inny format kwaterniona do transformations.py niz dostaje z VRPN
    # przy pierwszym uruchomieniu 
    # gdy nie ma poprzedniej orientacji 
    if(previous_orientation==0):
        previous_orientation=current_orientation
    
    rotation_quaternion=quaternion_multiply(quaternion_inverse(current_orientation),previous_orientation)
 
    print("ROTACJA:")
    print("\tkwaternion: (%f,%f,%f,%f)" % (rotation_quaternion[0],rotation_quaternion[1],
                                            rotation_quaternion[2],rotation_quaternion[3]))
                                   
    rotation_matrix = quaternion_matrix(rotation_quaternion)                             
    (rotation_angle,rotation_axis,point) = rotation_from_matrix(rotation_matrix)

    print("\tangle=%f\taxis: (x=%f,y=%f,z=%f)\tpoint:" % (rotation_angle,rotation_axis[0],rotation_axis[1],rotation_axis[2]))

    # zapamietuje dane z obecnej orientacji
    previous_orientation=current_orientation
    
        
def force_handler(userdata, force):
    print "sila",force
    

PHANTOM_LOCATION = "phantom0@172.21.5.156"
previous_orientation=0
position=(0.0, 0.0, 0.0)

tracker = vrpn_Tracker.vrpn_Tracker_Remote(PHANTOM_LOCATION)
vrpn_Tracker.register_tracker_change_handler(tracker_handler)
vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker, None, vrpn_Tracker.get_tracker_change_handler())

button = vrpn_Button.vrpn_Button_Remote(PHANTOM_LOCATION)
vrpn_Button.register_button_change_handler(button_handler)
vrpn_Button.vrpn_Button_Remote.register_change_handler(button, None, vrpn_Button.get_button_change_handler())

forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(PHANTOM_LOCATION)
vrpn_ForceDevice.register_force_change_handler(force_handler)
vrpn_ForceDevice.vrpn_ForceDevice_Remote.register_force_change_handler(forceDevice, None, vrpn_ForceDevice.get_force_change_handler())

point=[0,0,0]

while True:
    tracker.mainloop()
    button.mainloop()
    forceDevice.mainloop()

    if True:
	force=50	# sila (skalar)
        forceDevice.setFF_Origin(position[0], position[1], position[2])
        forceDevice.setFF_Force(force*(point[0]-position[0]), force*(point[1]-position[1]), force*(point[2]-position[2]))
        forceDevice.setFF_Jacobian(force,0,0, 0,force,0, 0,0,force)
        forceDevice.setFF_Radius(0.1)
        forceDevice.sendForceField()
            

