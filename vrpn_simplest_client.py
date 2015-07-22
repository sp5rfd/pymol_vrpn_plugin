# Program demonstracyjny w najbardziej elementarny sposob pokazuje jak polaczyc 
# sie z serwerem vrpn i odebrac z niego wszystkie niezbedne do dalszej pracy dane
#
# Demostration program that shows (probably...) the simples way to get data
# from VRPN server using vrpn_Tracker and vrpn_Button modules.
#
# @author 'Pawel Tomaszewski'
# @date ?

import sys
sys.path.append("vrpn_lib/")        # sciezka do biblioteki vrpn_lib

import vrpn_Tracker
import vrpn_Button

from threading import Thread

def handle_tracker(userdata, tracker):
    print tracker

def handle_button(userdata, button):
    button_number = button[0]
    status = button[1]

    if(status == 1):
        print "Button ", button_number, " pressed"
    else:
        print "Button ", button_number, " released"
        
class VRPNClient(Thread):
    tracker = vrpn_Tracker.vrpn_Tracker_Remote("phantom0@localhost")
    button = vrpn_Button.vrpn_Button_Remote("phantom0@localhost")
    
    def __init__(this):
        Thread.__init__(this)
        
        vrpn_Tracker.register_tracker_change_handler(handle_tracker)
        vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(this.tracker, None, vrpn_Tracker.get_tracker_change_handler())
        
        vrpn_Button.register_button_change_handler(handle_button)
        vrpn_Button.vrpn_Button_Remote.register_change_handler(this.button, None, vrpn_Button.get_button_change_handler())
            
    def run(self):
        while 1:
            self.tracker.mainloop()
            self.button.mainloop()

vrpn = VRPNClient()
vrpn.start()