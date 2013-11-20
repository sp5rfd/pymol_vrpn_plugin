import vrpn_Tracker
import vrpn_Button

def handle_button(userdata, t):
    button_number = t[0]
    status = t[1]
    if(status == 1):
        print "przycisk ", button_number, " zostal wcisniety"
    else:
        print "przycisk ", button_number, " zostal puszczony"
        
def handle_tracker(userdata, b):
    print b
#    scale = 1000
#    print "id=", b[0]*scale, "pos_x=", b[1]*scale, "pos_y=", b[2]*scale, "pos_z=", b[3]*scale, ",e =", b[4]*scale, ",f =", b[5]*scale, ",g =", b[6]*scale

tracker = vrpn_Tracker.vrpn_Tracker_Remote("phantom0@localhost")
vrpn_Tracker.register_tracker_change_handler(handle_tracker)
vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker,None,vrpn_Tracker.get_tracker_change_handler())

button = vrpn_Button.vrpn_Button_Remote("phantom0@localhost")
vrpn_Button.register_button_change_handler(handle_button)
vrpn_Button.vrpn_Button_Remote.register_change_handler(button,None, vrpn_Button.get_button_change_handler())

while 1:
    tracker.mainloop()
    button.mainloop()
    