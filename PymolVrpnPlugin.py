# -*- coding: utf-8 -*-

"""
    This program was created in 2015-16 by Pawel Tomaszewski
    In cooperation with Biophysics Laboratory of Warsaw University
"""

import os
import sys
sys.path.append("/home/crooveck/workspace/LICENCJAT/python_vrpn")
sys.path.append(".")
from transformations import *
from Tkinter import *
from tkFileDialog import *
#from ttk import *
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
AUTO_ZOOMING = False

"""
    Phantom VRPN URL.
"""
PHANTOM_URL="phantom0@172.21.5.156"

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

"""
    center of mass of a loaded molecule
"""
molecule_com=[0,0,0]    
mapping=[]
regions={}

"""
    Global variables for atom info UI
"""
startButton = stopButton = urlEntry = 0
atomSymbol = atomX = atomY = atomZ = 0

"""
    GUI
"""
helloMsg="\
Witaj użytkowniku.\
\nW tej aplikacji masz możliwość dopasowania lokalnie optymalnych struktur\
\ncząsteczek chemicznych takich jak białka czy kwasy nukleinowe\
\nlklklk"

currentWindow=0
mappingFile=0
phantomIp=0
mainPdbStructure=0
templateFile=0
structurePdb=0

def simple_com(region_coordinates):
    # pobiera jako parametr liste z krotkami ze wspolrzednymi i zwraca srodek masy
    x, y, z = 0,0,0
    size = len(region_coordinates)
    
    for coordinate in region_coordinates:
        x += coordinate[0]
        y += coordinate[1]
        z += coordinate[2]
        
    return (x/size, y/size, z/size)

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
    cmd.translate(vector=[(x0-x), (y0-y), (z0-z)], object="helix", camera=0)
    x = x0
    y = y0
    z = z0
    
#   ROTACJE 
    global previous_orientation
    # bierzacy stan - orientacja
    orientation=(tracker[7],tracker[4],tracker[5],tracker[6])   # inny format kwaterniona do transformations.py niz dostaje z VRPN
    # przy pierwszym uruchomieniu 
    # gdy nie ma poprzedniej orientacji 
    if(previous_orientation == 0):
        previous_orientation=orientation

    rotation_quaternion=quaternion_multiply(quaternion_inverse(previous_orientation),orientation)
    previous_orientation=orientation
    
    rotation_matrix = quaternion_matrix(rotation_quaternion) # Return homogeneous rotation matrix from quaternion.
    (rotation_angle,rotation_axis,point) = rotation_from_matrix(rotation_matrix)

    cmd.rotate(axis=[rotation_axis[0],rotation_axis[1],rotation_axis[2]], 
            angle=(rotation_angle*180/math.pi), origin=[x,y,z], object="helix", camera=0)


def button_handler(u, button):
    # button[0] - numer przycisku (0-gorny,1-dolny)
    # button[1] - status przycisku (0-puszczony,1-wcisniety)
    
    global AUTO_ZOOMING
    if(button[0]==0 and button[1]==0):
        AUTO_ZOOMING = False
    elif(button[0]==0 and button[1]==1):
        AUTO_ZOOMING = True
        
    if(button[0]==1 and button[1]==0):
        print "przycisk drugi puszczony"
        
    elif(button[0]==1 and button[1]==1):
        print "przycisk drugi wcisniety"
    
    
def force_handler(u, force):
#    print "force",force
    abc='test'
    
def draw_template_structure(template_pdb_file):
#    pointer = [
#        CONE, 0,0,0, 0,0,10,   #x1, y1, z1, x2, y2, z2
#        0.0, 1,                                   # Radius 1, 2
#        1, 0, 1,                                    # RGB Color 1
#        1, 1, 0,                                    # RGB Color 2
#        1.0, 1.0 ]                                  # Caps 1 & 2
#        
#    cmd.load_cgo(pointer, "helix")

    cmd.load(template_pdb_file,"helix")   # laduje wskaxnik
    helix_com=cmd.centerofmass("helix") # licze COM wskaxnika
    # centruje wskaxnik (przenosze go do zera)
    cmd.translate(vector=[-helix_com[0], -helix_com[1], -helix_com[2]], object="helix", camera=0)
    
def draw_xyz_axes(x0, y0, z0):
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
    
def draw_molecule(molecule_pdb_file):
    # laduje czasteczke
    cmd.load(molecule_pdb_file,"molecule")
    # licze jej centrum masy
    global molecule_com
    molecule_com=cmd.centerofmass("molecule")
    # przesuwam ja na srodek ekranu, srodek ciezkosci na (x,y,z)=(0,0,0)
    cmd.translate(vector=[-molecule_com[0], -molecule_com[1], -molecule_com[2]], object="molecule", camera=0)
    
    # pobieram liste pozycji 3D atomow w czasteczce
    stored.pos = []                                                                                                                
    cmd.iterate_state(1, "molecule", "stored.pos.append((x,y,z,elem,chain+resi))")
    

def load_mapping_file(mapping_file):
    file=open(mapping_file,"r")
    
    global mapping
    for line in file:
        mapping.append([line.split()[0],line.split()[1],0])
    file.close()
    
    # na ostatnie pole w mapping wstawiam COM obliczony dla kazdego nukleotydu
    for nucleotyde in mapping:  # iteruje po wszystkich liniach z pliku mapujacego
        # pobieram atomy nalezace do poszczegolnych nukleotydow
        nucl_atoms = [[atom[0],atom[1],atom[2]] for atom in stored.pos if (atom[4]==nucleotyde[1])]
        nucleotyde[2]=simple_com(nucl_atoms) # srodek masy dla nukleotydu
        
    print mapping
    
def calculate_regions_com():
    # zliczam ilosc nukleotydow w helisie wzorcowej
    # UWAGA: tutaj zakladam, ze wzorcowa helisa sklada sie z dwoch lancuchow o 
    # tej samej dlugosci (ilosci nukleotydow). To oznacza, ze szukam regionow 
    # o dlugosci jednego lancucha helisy, czyli polowy wszystkich nukleotydow
    # z tej helisy.
    
    unique_nucl=set()
    cmd.iterate_state(1,"helix","unique_nucl.add(chain+resi)",space={'unique_nucl':unique_nucl})
    M=len(mapping)        # ilosc nukleotydow w BADANEJ czasteczce
    N=len(unique_nucl)/2  # polowa wszystkich nukleotydow z WZORCOWEJ czasteczki
    
    # wyszukiwanie regionow
    for m in range(0,M-N+1): # -1 jesli blad
        region=()   # inicjuje pusty tuple
        region_coords=[]
        for n in range(0,N): # -1 jesli blad
            if mapping[m+n][0]=='0':
                break
            region=region+(mapping[m+n][1],)
            region_coords.append(mapping[m+n][2])
            if n==(N-1):
                #znaleziono region w badanej czasteczke pasujacy do czasteczki wzorcowej
#                print "JEST REGION: ", m, region, region_coords
                # dodaje znaleziony region do tablicy regions
                regions[region]=simple_com(region_coords)
#                regions.append(region)
            
#    print regions

def find_closest_atom(x0,y0,z0):
    if(len(stored.pos)==0):
        zero=[0,0,0]
        # zeruje interfejs - atomX,Y i Z to pola w GUI
        atomX.delete(0,'end')
        atomX.insert(0, zero[0])
        atomY.delete(0,'end')
        atomY.insert(0, zero[1])
        atomZ.delete(0,'end')
        atomZ.insert(0, zero[2])
        return zero
    
    minimumDistance=sys.float_info.max     # poczatkowa wartosc minimalna powinna byc duza
    closestAtomDistance=0                        # index najblizszego atomu
    # liczymy najblizszy atom 
    for atomNumber in xrange(0,len(stored.pos)):
        xDistance = (stored.pos[atomNumber][0]-molecule_com[0])-x0
        yDistance = (stored.pos[atomNumber][1]-molecule_com[1])-y0
        zDistance = (stored.pos[atomNumber][2]-molecule_com[2])-z0
        distance=sqrt(math.pow(xDistance,2)+math.pow(yDistance,2)+math.pow(zDistance,2))
        
        if(distance<minimumDistance):
            minimumDistance=distance
            closestAtomDistance=atomNumber
    
    # zapamietuje wsp. nablizszego atomu
    closestAtomX=stored.pos[closestAtomDistance][0]-molecule_com[0]
    closestAtomY=stored.pos[closestAtomDistance][1]-molecule_com[1]
    closestAtomZ=stored.pos[closestAtomDistance][2]-molecule_com[2]
    
    # aktualizacja interfejsu
    atomX.delete(0,'end')
    atomX.insert(0, round(closestAtomX,3))
#    atomX.insert(0, round(stored.pos[minNumber][0],3))
    atomY.delete(0,'end')
    atomY.insert(0, round(closestAtomY,3))
#    atomY.insert(0, round(stored.pos[minNumber][1],3))
    atomZ.delete(0,'end')
    atomZ.insert(0, round(closestAtomZ,3))
#    atomZ.insert(0, round(stored.pos[minNumber][2],3))
    atomSymbol.delete(0, 'end')
    atomSymbol.insert(0, stored.pos[closestAtomDistance][3])
    
#    return (stored.pos[minNumber][0]/scale, stored.pos[minNumber][1]/scale, stored.pos[minNumber][2]/scale)
    return (closestAtomX/scale, closestAtomY/scale, closestAtomZ/scale)
    
    
def find_closest_region(x0,y0,z0):
    # jesli nie ma regionow, to zwroc najblizszy atom
    if len(regions)==0:
        return find_closest_atom(x0, y0, z0)
    
    min_distance=sys.float_info.max  # startujemy od najwiekszej mozliwej wielkosci
    closest_region_x,closest_region_y,closest_region_z = 0,0,0
    
    for region in regions:      # iteruje po regionach
        coords=regions[region]  # pobieram z mapy regionow wspolrzedne
        x_dist = (coords[0]-molecule_com[0])-x0
        y_dist = (coords[1]-molecule_com[1])-y0
        z_dist = (coords[2]-molecule_com[2])-z0
        distance=sqrt(math.pow(x_dist,2)+math.pow(y_dist,2)+math.pow(z_dist,2))
        
        if(distance<min_distance):
            min_distance=distance
            closest_region_x = coords[0]-molecule_com[0]
            closest_region_y = coords[1]-molecule_com[1]
            closest_region_z = coords[2]-molecule_com[2]
    
    return (closest_region_x/scale,closest_region_y/scale,closest_region_z/scale)
    
def vrpn_client():
    global mappingFile,templateFile,phantomIp
    
#    tracker = vrpn_Tracker.vrpn_Tracker_Remote(PHANTOM_URL)
    tracker = vrpn_Tracker.vrpn_Tracker_Remote(phantomIp.get())
    vrpn_Tracker.register_tracker_change_handler(tracker_handler)
    vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker, None, vrpn_Tracker.get_tracker_change_handler())

#    button = vrpn_Button.vrpn_Button_Remote(PHANTOM_URL)
    button = vrpn_Button.vrpn_Button_Remote(phantomIp.get())
    vrpn_Button.register_button_change_handler(button_handler)
    vrpn_Button.vrpn_Button_Remote.register_change_handler(button, None, vrpn_Button.get_button_change_handler())

#    forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(PHANTOM_URL)
    forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(phantomIp.get())
    vrpn_ForceDevice.register_force_change_handler(force_handler)
    vrpn_ForceDevice.vrpn_ForceDevice_Remote.register_force_change_handler(forceDevice, None, vrpn_ForceDevice.get_force_change_handler())
    
    draw_xyz_axes(0,0,0)
    draw_template_structure(templateFile.get())
    draw_molecule("1fg0.pdb")
    load_mapping_file(mappingFile.get())
    calculate_regions_com()
    
    startButton['state']="disabled"
    stopButton['state']="normal"
    urlEntry['state']="disabled"
    sleep(1)
    
    while IS_RUNNING:
        tracker.mainloop()
        button.mainloop()
        forceDevice.mainloop()
        
        # znajduje najblizszy punkt do aktualnej pozycji wskaxnika PyMol
#        point = find_closest_atom(x,y,z)
        
        # znajduje nablizszy region do w czasteczce do ktorego przyciagam wzorzec
        point =  find_closest_region(x,y,z)

        force=100   # wielkosc sily |F|
        forceX = (point[0]-trackerX)    # wektor sily X
        forceY = (point[1]-trackerY)    # j.w. Y
        forceZ = (point[2]-trackerZ)    # j.w. Z

        forceDevice.setFF_Origin(trackerX, trackerY, trackerZ)
        forceDevice.setFF_Force(force*forceX, force*forceY, force*forceZ)
        forceDevice.setFF_Jacobian(force,0,0, 0,force,0, 0,0,force)
        forceDevice.setFF_Radius(0.1)
        forceDevice.sendForceField()

        # rysuje linie laczaco wskaznik z najblizszym atomem
        cmd.delete('link')
        cmd.load_cgo([CYLINDER, x, y, z, point[0]*scale, point[1]*scale, point[2]*scale, 0.1, 255, 255, 255, 255, 255, 255], 'link')

        if(not AUTO_ZOOMING):
            cmd.zoom('all')

    print "Finishing work..."
    startButton['state']="normal"
    stopButton['state']="disabled"
    urlEntry['state']="normal"

def run():
    global IS_RUNNING, PHANTOM_URL
    IS_RUNNING = True
    PHANTOM_URL=urlEntry.get()
    
    thread.start_new_thread(vrpn_client, ())
    
def stop():
    global IS_RUNNING
    IS_RUNNING = False
    
def statsWindow():
    currentWindow = Tk()
    currentWindow.title("PyMOL VRPN Plugin v1.0")
    currentWindow.geometry("370x280+200+100")
    currentWindow.resizable(False, False)
    currentWindow.call('wm', 'attributes', '.', '-topmost', '1')
    
    vrpnGroup = LabelFrame(currentWindow, text=" VRPN CFG. ", width=350, height=90)
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
    
    atomGroup = LabelFrame(currentWindow, text=" ATOM INFO ", width=350, height=150)
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
    
    currentWindow.mainloop()
    

def chooseTemplateFile():
    global templateFile
    templateFile.set(askopenfilename())
    print templateFile.get()

def chooseMappingFile():
    global mappingFile
    mappingFile.set(askopenfilename())
    print mappingFile.get()

def openStatsWindow():
    global currentWindow
    currentWindow.destroy()
    statsWindow()
    
def openConfigWindow():
    global currentWindow
    currentWindow.destroy()
    configWindow()
    
def chooseMainStructure():
    //todo
def configWindow():
    global currentWindow,templateFile,mappingFile,phantomIp,mainPdbStructure
    
    currentWindow = Toplevel()
    currentWindow.title("Eksplorator lokalnych podobieństw struktur przestrzennych")
    
    templateFile=StringVar(value=os.getcwd()+"/")
    mappingFile=StringVar(value=os.getcwd()+"/")
    mainPdbStructure=StringVat(value=os.getcwd()+"/")
    phantomIp=StringVar(value=PHANTOM_URL)
    
    w=640
    h=480
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
#    Wybór wzorca
    group=LabelFrame(currentWindow,text="Wzorzec",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    message="Wzorzec jest strukturą, którą będziemy próbowali dopasować do cząsteczki bazowej.\
    \nWzorzec może stanowić wycinek cząsteczki bazowej, np. jakaś struktura drugorzędowa"
    
    label=Label(group,text=message,bg="green",anchor=W)
    label.pack(fill=BOTH)
    
    fileName=Entry(group,textvariable=templateFile,width=50,state="readonly")
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik",command=chooseTemplateFile)
    fileChooser.pack(side=LEFT)
    
#    Wybór pliku mapowania
    group=LabelFrame(currentWindow,text="Plik mapowania",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    label=Label(group,text="Tutaj wybierz plik mapowania",bg="green",anchor=W)
    label.pack(fill=BOTH)
    
    fileName=Entry(group,textvariable=mappingFile,width=50,state="readonly")
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik",command=chooseMappingFile)
    fileChooser.pack(side=LEFT)
    
#    Wybór identyfikatora PDB
    group=LabelFrame(currentWindow,text="Identyfikator PDB",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    
    label=Label(group,text="Tutaj wybierz plik ",bg="green",anchor=W)
    label.pack(fill=BOTH)
        
    fileName=Entry(group,textvariable=mainPdbStructure,width=50,state="readonly")
    fileName.pack(pady=5,side=LEFT)
    
    fileChooser=Button(group,text="Wybierz plik",command=chooseMainStructure)
    fileChooser.pack(side=LEFT)
    
    #    ustawianie adresu IP serwera VRPN
    group=LabelFrame(currentWindow,text="Adres IP serwera VRPN",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    vrpnIp=Entry(group,justify=CENTER,textvariable=phantomIp)
    vrpnIp.pack(pady=5,side=LEFT)
    
    group=Frame(currentWindow)
    group.pack(padx=5,expand=TRUE)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    
    closeButton=Button(group,text="Anuluj",command=currentWindow.destroy)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=openStatsWindow)
    nextButton.pack()
    
    currentWindow.mainloop();
    
def helloWindow():
    global currentWindow
    currentWindow = Toplevel()
    currentWindow.title("Eksplorator lokalnych podobieństw struktur przestrzennych")
    
    w=640
    h=480
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    
    group=LabelFrame(currentWindow,text="Witaj",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5,expand=True)
    
    label=Label(group,text=helloMsg,bg="green")
    label.pack(fill=BOTH,side=LEFT)
    
    dnaImage=PhotoImage(file="dna.gif")
    
    label=Label(group,image=dnaImage)
    label.pack(fill=BOTH)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    
    closeButton=Button(group,text="Anuluj",command=currentWindow.destroy)
    closeButton.pack(side=RIGHT)
    
    nextButton=Button(group,text="Dalej",command=openConfigWindow)
    nextButton.pack()
    
    currentWindow.mainloop();
    
    
def __init__(self):
    print "__init__"
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
                             command = lambda s=self: helloWindow())
#    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN', label = 'VRPN Plugin', 
#                             command = lambda s=self: build_gui())
                             
