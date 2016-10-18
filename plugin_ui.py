from Tkinter import *
from ttk import *
import thread

IS_RUNNING=False
PHANTOM_URL="phantom0@127.0.0.1"
startButton=stopButton=urlEntry=0
atomSymbol=atomX=atomY=atomZ=0

def vrpn_client():
    while IS_RUNNING:
        atomSymbol.delete(0,END)
        atomSymbol.insert(0,'H')

def run():
    global IS_RUNNING
    IS_RUNNING = True
    PHANTOM_URL=urlEntry.get()
    startButton['state']=DISABLED
    stopButton['state']=NORMAL
    
    thread.start_new_thread(vrpn_client, ())
    
    print "running...", IS_RUNNING, PHANTOM_URL

def stop():
    global IS_RUNNING
    IS_RUNNING = False
    startButton['state']=NORMAL
    stopButton['state']=DISABLED
    
    print "stopping...", IS_RUNNING
    
def build_gui():
    window = Tk()
    window.title("PyMOL VRPN Plugin v1.0")
    window.geometry("370x280+200+100")
    window.resizable(False, False)
    window.call('wm', 'attributes', '.', '-topmost', '1')
    
    vrpnGroup = LabelFrame(window, text=" VRPN CFG. ", width=350, height=90)
    vrpnGroup.grid(row=0, padx=10, pady=10)
    vrpnGroup.grid_propagate(False)

    Label(vrpnGroup, text="PHANTOM URL: ").grid(row=0, padx=10, pady=10)
    global startButton, stopButton, urlEntry
    urlEntry=Entry(vrpnGroup, width=25, justify=CENTER)
    urlEntry.insert(0,PHANTOM_URL)
    urlEntry.grid(row=0, column=1, columnspan=2)
    startButton=Button(vrpnGroup, text="START", command=run)
    startButton.grid(row=1, column=1, columnspan=2, sticky=W)
    stopButton=Button(vrpnGroup, text="STOP", command=stop, state=DISABLED)
    stopButton.grid(row=1, column=1, columnspan=2, sticky=E)
    
    atomGroup = LabelFrame(window, text=" ATOM INFO ", width=350, height=150)
    atomGroup.grid(row=1, padx=10, pady=10)
    atomGroup.grid_propagate(False)
    Label(atomGroup, text="Symbol chemiczny:").grid(row=0, padx=10, pady=5)
    global atomSymbol, atomX, atomY, atomZ
    atomSymbol=Entry(atomGroup, width=15, justify=CENTER)
    atomSymbol.grid(row=0, column=1)
    Label(atomGroup, text="Pozycja X=").grid(row=1, sticky=E, padx=10, pady=5)
    atomX=Entry(atomGroup, width=15, justify=CENTER)
    atomX.grid(row=1, column=1)
    Label(atomGroup, text="Pozycja Y=").grid(row=2, sticky=E, padx=10, pady=5)
    atomY=Entry(atomGroup, width=15, justify=CENTER)
    atomY.grid(row=2, column=1)
    Label(atomGroup, text="Pozycja Z=").grid(row=3, sticky=E, padx=10, pady=5)
    atomZ=Entry(atomGroup, width=15, justify=CENTER)
    atomZ.grid(row=3, column=1)
    
    window.mainloop()

if __name__ == "__main__":
    build_gui()