from trace import threading
from threading import Thread
import vrpn_Tracker
import vrpn_Button
    
def handle_button(userdata, b):
    button_number = b[0]
    status = b[1]
    
    if(status == 1):
        print "przycisk ", button_number, " zostal wcisniety"
    else:
        print "przycisk ", button_number, " zostal puszczony"

def handle_tracker(userdata, t):
    print t
        
class VRPNClient(Thread):
    tracker = vrpn_Tracker.vrpn_Tracker_Remote("phantom0@localhost")
    button = vrpn_Button.vrpn_Button_Remote("phantom0@localhost")
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        vrpn_Tracker.register_tracker_change_handler(handle_tracker)
        vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(self.tracker, None, vrpn_Tracker.get_tracker_change_handler())
        
        vrpn_Button.register_button_change_handler(handle_button)
        vrpn_Button.vrpn_Button_Remote.register_change_handler(self.button, None, vrpn_Button.get_button_change_handler())
        
        self.start()
            
    def run(self):
        while 1:
            self.tracker.mainloop()
            self.button.mainloop()
 
            
vrpn = VRPNClient()