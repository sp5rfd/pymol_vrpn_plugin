from Tkinter import Tk
from Tkinter import *

class GUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("640x480+100+100")
        
        Label(text="Wspolrzedna X: ").grid(row=0)
        Label(text="Wspolrzedna Y: ").grid(row=1)
        Label(text="Wspolrzedna Y: ").grid(row=2)
        
        self.xCoord = Entry()
        self.xCoord.grid(row=0, column=1)
        yCoord = Entry().grid(row=1, column=1)
        yCoord = Entry().grid(row=2, column=1)
        
        xButton = Button(text="x++")
        xButton.grid(row=0, column=2)
        xButton.bind("<Button-1>", self.xIncrement)
        
        yButton = Button(text="y++").grid(row=1, column=2)
        zButton = Button(text="z++").grid(row=2, column=2)

        self.mainloop()

    def xIncrement(self, event=None):
        
        print self.xCoord.get()
GUI()
