# -*- coding: utf-8 -*-

"""
    Kod źródłowy pracy licencjackiej zatytułowanej:
    "Interaktywna eksploracja i dopasowanie lokalnie optymalnych struktur biopolimerów
    z wykorzystaniem metod wirtualnej rzeczywistości.".
    Praca powstała na kierunku Bioinformatyka i Biologia Systemów 
    Wydziału Matematyki, Informatyki i Mechaniki Uniwersytetu Warszawskiego.

    Autorem programu jest Paweł Tomaszewski. Praca powstała w pracowni udostępnionej
    przez Zakład Biofizyki Wydziału Fizyki Uniwersytetu Warszawskiego.
"""

import os
import sys
sys.path.append("~/workspace/LICENCJAT/python_vrpn")
sys.path.append(".")
from transformations import *
from Tkinter import *
from tkFileDialog import *
from pymol import *
from pymol.cgo import *
from time import *
import vrpn_Tracker
import vrpn_Button
import vrpn_ForceDevice
from math import *

# Flagi wykorzystywane w pętli głównej programu.
IS_RUNNING = False          # Flaga sterująca działanie pętli głównej programu
AUTO_ZOOMING = False        # Flaga sterująca opcją auto-zoom
REGION_COLORING = True      # Flaga sterująca kolorowaniem regionów
FORCES_ENABLED = False      # Flaga sterująca sprzężeniem zwrotnym

# Współrzędne w przestrzeni urządzenia Phantom Omni
trackerX = trackerY = trackerZ = 0
# Współrzędne w przestrzeni PyMOL
x = y = z = 0 
# Współczynnik skalujący translacje pomiędzy przestrzeniami urządznia Phantom Omni oraz PyMOL
scale=750

# Środek ciężkości całej cząsteczki
molecule_com=[0,0,0]  
# Środek ciężkości struktury wzorca
templateCOM=(0,0,0)
# Środek ciężkości struktury regionu
regionCOM=(0,0,0)

# Kwaterion reprezentujący poprzednią (zachowaną) orientację
previous_orientation=0

mapping=[]
regions={}

currentWindow=0
phantomIp=0

# Zmienne przechowujące dane wejściowe
targetStructureFile=0
templateStructureFile=0
structureMappingFile=0

# Zmienne pomocnicze do UI
regionId=regionX=regionY=regionZ=regionTemplateDistance=rmsdEntry=0

# Prosta funkcja obliczająca środek masy (COM) zadanych punktów w przestrzeni
def simple_com(region_coordinates):
    # pobiera jako parametr liste z krotkami ze wspolrzednymi i zwraca srodek masy
    x, y, z = 0,0,0
    size = len(region_coordinates)
    
    for coordinate in region_coordinates:
        x += coordinate[0]
        y += coordinate[1]
        z += coordinate[2]
        
    return (x/size, y/size, z/size)

# Handler obsługujący zdarzenia dot. trackera (rotacje, translacje)
def tracker_handler(u, tracker):
    global trackerX, trackerY, trackerZ
    trackerX = tracker[1]
    trackerY = tracker[2]
    trackerZ = tracker[3]
    
#    print trackerX,trackerY,trackerZ
    
#   TRANSLACJE:
    x0 = trackerX*scale
    y0 = trackerY*scale
    z0 = trackerZ*scale
#   funkcja dokonujaca przeksztalcenia - transjacji
    global x, y, z
    cmd.translate(vector=[(x0-x), (y0-y), (z0-z)], object="template", camera=1)
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
            angle=(rotation_angle*180/math.pi), origin=[templateCOM[0],templateCOM[1],templateCOM[2]], object="template", camera=1)

# Handler obsługujący zdarzenia dot. przycisków
def button_handler(u, button):
    # button[0] - numer przycisku (0-gorny,1-dolny)
    # button[1] - status przycisku (0-puszczony,1-wcisniety)
    
    global AUTO_ZOOMING
    if(button[0]==0 and button[1]==0):
        AUTO_ZOOMING = False
    elif(button[0]==0 and button[1]==1):
        AUTO_ZOOMING = True
            
    # wykonuje dopasowanie i translacje wzorca nad regionem
    if(button[0]==1 and button[1]==1):
        
        cmd.align("template","region")
        
        reg_com=cmd.centerofmass("region")
        temp_com=cmd.centerofmass("template")
        
        cmd.translate(object="template", vector=[reg_com[0]-temp_com[0],
            reg_com[1]-temp_com[1],reg_com[2]-temp_com[2]], camera=0)
        
# Handler obsługujący zdarzenia związane ze sprzężeniem zwrotnym 
# (brak implementacji, patrz: pętla główna programu)
def force_handler(u, force):
    return None
    
# Funkcja rysujca osie układu współrzędnych
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

# Funkcja rysuje strukturę wzorcową (template)
def draw_template_structure(template_pdb_file):
    cmd.load(template_pdb_file,"template")
    cmd.hide("lines","template")
    cmd.show("cartoon","template")
    cmd.color("green","template")
    
    template_com=cmd.centerofmass("template")
    # centruje wskaxnik (przenosze go do zera)
    cmd.translate(vector=[-template_com[0], -template_com[1], -template_com[2]], object="template", camera=0)

# Funkcja rysuje strukturę celu (target)
def draw_target_structure(target_pdb_file):
    # laduje czasteczke
    cmd.load(target_pdb_file,"target")
    cmd.hide("lines","target")
    cmd.show("cartoon","target")
    cmd.color("red","target")
    
    # licze jej centrum masy
    global molecule_com
    molecule_com=cmd.centerofmass("target")
    # przesuwam ja na srodek ekranu, srodek ciezkosci na (x,y,z)=(0,0,0)
    cmd.translate(vector=[-molecule_com[0], -molecule_com[1], -molecule_com[2]], object="target", camera=0)
    
    # pobieram liste pozycji 3D atomow w czasteczce
    stored.pos = []                                                                                                                
    cmd.iterate_state(1, "target", "stored.pos.append((x,y,z,elem,chain,resi))")
    
# Funkcja obsługująca ładowanie pliku mapujacego
def load_mapping_file(mapping_file):
    file=open(mapping_file,"r")
    
    global mapping
    mapping=[]

    for line in file:
        mapping_symbol=line.split()[0]
        chain=line.split()[1][0]
        resi=line.split()[1][1:]
        mapping.append([mapping_symbol,chain,resi,0])
    file.close()
    
    # na ostatnie pole w mapping wstawiam COM obliczony dla kazdego nukleotydu
    for nucleotyde in mapping:  # iteruje po wszystkich liniach z pliku mapujacego
        # pobieram atomy nalezace do poszczegolnych nukleotydow
        nucl_coords = [[atom[0],atom[1],atom[2]] for atom in stored.pos if (atom[5]==nucleotyde[2])]
        nucleotyde[3]=simple_com(nucl_coords) # srodek masy dla nukleotydu
        
    print "SKONCZYLEM LADOWANIE MAPOWANIA"
    
# Obliczam środek ciężkości wszystkich wykrytych regionów
def calculate_regions_com():
    # zliczam ilosc nukleotydow w helisie wzorcowej
    # UWAGA: tutaj zakladam, ze wzorcowa helisa (czy struktura) sklada sie z dwoch lancuchow o 
    # tej samej dlugosci (ilosci nukleotydow). To oznacza, ze szukam regionow 
    # o dlugosci jednego lancucha helisy, czyli polowy wszystkich nukleotydow
    # z tej helisy.
    
    unique_nucl=set()
    cmd.iterate_state(1,"template","unique_nucl.add((chain,resi))",space={'unique_nucl':unique_nucl})
    M=len(mapping)        # ilosc nukleotydow w BADANEJ czasteczce
    N=len(unique_nucl)/2  # polowa wszystkich nukleotydow z WZORCOWEJ czasteczki
    
    # wyszukiwanie regionow
    for m in range(0,M-N+1): # -1 jesli blad
        region=()   # inicjuje pusty tuple
        region_coords=[]
        for n in range(0,N): # -1 jesli blad
            if mapping[m+n][0]=='0':
                break
            region=region+(mapping[m+n][2],)
            region_coords.append(mapping[m+n][3])
            if n==(N-1):
                #znaleziono region w badanej czasteczke pasujacy do czasteczki wzorcowej
#                print "JEST REGION: ", m, region, region_coords
                # dodaje znaleziony region do tablicy regions
                regions[region]=simple_com(region_coords)
            
#    print regions

# Obliczam środek ciężkości wszystkich wykrytych regionów (po nowemu)
def new_calculate_regions_com():    
    unique_nucl=set()
    cmd.iterate_state(1,"template","unique_nucl.add((chain,resi))",space={'unique_nucl':unique_nucl})
    M=len(mapping)        # ilosc nukleotydow z czasteczki celu
    N=len(unique_nucl)  # wszystkie nukleotydy z WZORCOWEJ czasteczki
    
    # wyszukiwanie regionow
    for m in range(0,M-N+1): # -1 jesli blad
        region=()   # inicjuje pusty tuple
        region_coords=[]
        for n in range(0,N): # -1 jesli blad
            if mapping[m+n][0]=='0':
                break
            region=region+(mapping[m+n][2],)
            region_coords.append(mapping[m+n][3])
            if n==(N-1):
                # znaleziono region w badanej czasteczke pasujacy do czasteczki wzorcowej
#                print "JEST REGION: ", m, region, region_coords
                # dodaje znaleziony region do tablicy regions
                regions[region]=simple_com(region_coords)
            

# Funkcja znajdująca najbliższy atom do zadanej pozycji
def find_closest_atom(x0,y0,z0):
    if(len(stored.pos)==0):
        return [0,0,0]
    
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
    
    return (closestAtomX/scale, closestAtomY/scale, closestAtomZ/scale)
    
# Funkcja znajduje najbliższy region do zadanej pozycji
def find_closest_region(x0,y0,z0):
    # jesli nie ma regionow, to zwroc najblizszy atom
    if len(regions)==0:
        return find_closest_atom(x0, y0, z0)
    
    min_distance=sys.float_info.max  # startujemy od najwiekszej mozliwej wielkosci
    closestX,closestY,closestZ = 0,0,0
    closestRegionId=0
    
    for region in regions:      # iteruje po regionach
        coords=regions[region]  # pobieram z mapy regionow wspolrzedne
        x_dist = (coords[0]-molecule_com[0])-x0
        y_dist = (coords[1]-molecule_com[1])-y0
        z_dist = (coords[2]-molecule_com[2])-z0
        distance=sqrt(math.pow(x_dist,2)+math.pow(y_dist,2)+math.pow(z_dist,2))
        
        if(distance<min_distance):
            min_distance=distance
            closestRegionId=region
            closestX = coords[0]-molecule_com[0]
            closestY = coords[1]-molecule_com[1]
            closestZ = coords[2]-molecule_com[2]
    
    # tworze nowy selection do najblizszego regionu
    selectCommand="resi "
    for resi in closestRegionId: 
        selectCommand+=resi+","
        
    if REGION_COLORING:
        cmd.color("red","target")    
        cmd.select("region",selectCommand)
        cmd.color("yellow","region")
    else:
        cmd.color("red","target")
        cmd.select("region",selectCommand)
    
    return [closestRegionId,(closestX/scale),(closestY/scale),(closestZ/scale),min_distance]
    
# Główna funkcja wykonawcza programu
def vrpn_client():
    global structureMappingFile,templateStructureFile,phantomIp
    
    tracker = vrpn_Tracker.vrpn_Tracker_Remote(phantomIp.get())
    vrpn_Tracker.register_tracker_change_handler(tracker_handler)
    vrpn_Tracker.vrpn_Tracker_Remote.register_change_handler(tracker, None, vrpn_Tracker.get_tracker_change_handler())

    button = vrpn_Button.vrpn_Button_Remote(phantomIp.get())
    vrpn_Button.register_button_change_handler(button_handler)
    vrpn_Button.vrpn_Button_Remote.register_change_handler(button, None, vrpn_Button.get_button_change_handler())

    forceDevice = vrpn_ForceDevice.vrpn_ForceDevice_Remote(phantomIp.get())
    vrpn_ForceDevice.register_force_change_handler(force_handler)
    vrpn_ForceDevice.vrpn_ForceDevice_Remote.register_force_change_handler(forceDevice, None, vrpn_ForceDevice.get_force_change_handler())
    
    draw_xyz_axes(0,0,0)
    
    draw_template_structure(templateStructureFile.get())
    draw_target_structure(targetStructureFile.get())
    load_mapping_file(structureMappingFile.get())
    
    new_calculate_regions_com()
    
    global regionId, regionX, regionY, regionZ
    global x,y,z
    global templateCOM,regionCOM
    
    sleep(1)    # czekam az sie wszystko polaczy i narysuje
    
    # główna pętl programu
    while IS_RUNNING:
        if(not AUTO_ZOOMING):
            cmd.zoom('all')
            
        tracker.mainloop()
        forceDevice.mainloop()
        button.mainloop()
        
        # obliczam aktualny srodek ciezkosci wzorca
        templateCOM=cmd.centerofmass("template")
        
        # znajduje nablizszy dla wzorca region w czasteczce celu 
        # do ktorego bede przyciagac wzorzec/wzkaznik
        region=find_closest_region(templateCOM[0],templateCOM[1],templateCOM[2]) 
        
        regionCOM=cmd.centerofmass("region")
        
        print "RMSD: ", cmd.rms_cur("template","region")
        
        # aktualizacja interfejsu
        regionId.delete(0,'end')    #todo: zmienic na zmienna textvariable
        regionId.insert(0,region[0])
        regionX.delete(0,'end')
        regionX.insert(0,region[1])
        regionY.delete(0,'end')
        regionY.insert(0,region[2])
        regionZ.delete(0,'end')
        regionZ.insert(0,region[3])
        regionTemplateDistance.delete(0,'end')
        regionTemplateDistance.insert(0,region[4])
        
        if FORCES_ENABLED:
            force=100   # skalarna wartosc sily |F|       
            forceX = (region[1]-trackerX)    # wersor X sily
            forceY = (region[2]-trackerY)    # wersor Y sily
            forceZ = (region[3]-trackerZ)    # wersor Z sily
            forceDevice.setFF_Origin(trackerX, trackerY, trackerZ)
            forceDevice.setFF_Force(force*forceX, force*forceY, force*forceZ)
            forceDevice.setFF_Jacobian(force,0,0, 0,force,0, 0,0,force)
            forceDevice.setFF_Radius(0.1)
            forceDevice.sendForceField()
        else:
            forceDevice.setFF_Origin(0,0,0)
            forceDevice.setFF_Force(0,0,0)
            forceDevice.setFF_Jacobian(0,0,0, 0,0,0, 0,0,0)
            forceDevice.setFF_Radius(0.0)
            forceDevice.sendForceField()

        # rysuje linie laczaca wzorzec/wskaznik z najblizszym regionem/atomem
        cmd.delete('link')
        cmd.load_cgo([CYLINDER, templateCOM[0],templateCOM[1],templateCOM[2], (regionCOM[0]), (regionCOM[1]), (regionCOM[2]), 0.1, 255, 255, 255, 255, 255, 255], 'link')
#        cmd.load_cgo([CYLINDER, templateCOM[0],templateCOM[1],templateCOM[2], (region[1]*scale), (region[2]*scale), (region[3]*scale), 0.1, 255, 255, 255, 255, 255, 255], 'link')
            
    cmd.delete("*")
    x=y=z=0
    
def stop():
    global IS_RUNNING
    IS_RUNNING = False
    sleep(1)
    configWindow()
    
def doColorRegion():
    global REGION_COLORING
    
    if REGION_COLORING:
        REGION_COLORING=False
    else:
        REGION_COLORING=True
    
def doEnableForces():
    global FORCES_ENABLED
    
    if FORCES_ENABLED:
        FORCES_ENABLED=False
    else:
        FORCES_ENABLED=True
    
def statsWindow():    
    global currentWindow,IS_RUNNING
    IS_RUNNING = True
    thread.start_new_thread(vrpn_client, ())
    
    currentWindow.destroy()
    
    w=640
    h=400
    currentWindow=Tk()
    currentWindow.title("Interactive local structure alignment explorer")
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    currentWindow.attributes('-topmost', 1)
    currentWindow.resizable(False, False)
    currentWindow.grid_columnconfigure(0, weight=1)
    currentWindow.grid_columnconfigure(1, weight=1)
    
    global regionId, regionX, regionY, regionZ, regionTemplateDistance, rmsdEntry
    group=LabelFrame(currentWindow, text="Wspolrzedne")
    group.grid(column=0,padx=5,pady=5,sticky='WE')
    Label(group, text="ID regionu:",anchor=W).grid(row=0,column=0,sticky='WE')
    regionId=Entry(group, width=30, justify=CENTER)
    regionId.grid(row=0,column=1,sticky='W')
    Label(group, text="COM X regionu:",anchor=W).grid(row=1,column=0,sticky='WE')
    regionX=Entry(group, width=20, justify=CENTER)  # todo: odswiezac te pola po textvariable zamiast tego co jest
    regionX.grid(row=1,column=1,sticky='W')
    Label(group, text="COM Y regionu:",anchor=W).grid(row=2,column=0,sticky='WE')
    regionY=Entry(group, width=20, justify=CENTER)  # todo: jw.
    regionY.grid(row=2,column=1,sticky='W')
    Label(group, text="COM Z regionu:",anchor=W).grid(row=3,column=0,sticky='WE')
    regionZ=Entry(group, width=20, justify=CENTER)  # todo: jw.
    regionZ.grid(row=3,column=1,sticky='W')
    Label(group,text="Odleglosc wzorca i regionu:",anchor=W).grid(row=4,column=0,sticky="WE")
    regionTemplateDistance=Entry(group, width=20, justify=CENTER)  # todo: jw.
    regionTemplateDistance.grid(row=4,column=1,sticky='W')
    
    group=LabelFrame(currentWindow,text="Opcje")
    group.grid(column=1,row=0,sticky='NSWE',pady=5,padx=5)
    colors=Checkbutton(group,text="Koloruj region",command=doColorRegion)
    colors.select()
    colors.grid(row=0,sticky="W")
    Checkbutton(group,text="Projekcja sil",command=doEnableForces).grid(row=1,sticky="W")
    
    
    # RMSD
#    group=LabelFrame(currentWindow,text="Wykres RMSD (Root-mean-square diviation)")
#    group.grid(row=1,columnspan=2,sticky="NSWE",padx=5,pady=5)
#    rmsdEntry=Entry(group,width=20,justify=CENTER)
#    Label(group,text="\n\ntu bedzie wykres...\n\n").grid(sticky="WE")
    
#    spacer
    Frame(currentWindow).grid(sticky="NSWE")
    
#    przyciski
    group=Frame(currentWindow)
    group.grid(row=3,columnspan=2)
    stopButton=Button(group, text="STOP", command=stop)
    stopButton.grid()
    
    currentWindow.mainloop()

def chooseTemplateStructureFile():
    global templateStructureFile
    templateStructureFile.set(askopenfilename( filetypes=(("PDB", "*.pdb"), ("All files", "*.*")) ))
    print templateStructureFile.get()

def chooseStructureMappingFile():
    global structureMappingFile
    structureMappingFile.set(askopenfilename( filetypes=(("MAP", "*.map"), ("All files", "*.*")) ))
    print structureMappingFile.get()
    
def chooseTargetStructureFile():
    global targetStructureFile
    targetStructureFile.set(askopenfilename( filetypes=(("PDB", "*.pdb"), ("All files", "*.*")) ))
    print targetStructureFile.get()
    
def configWindow():
    global currentWindow,templateStructureFile,structureMappingFile,phantomIp,targetStructureFile

    currentWindow.destroy()

    w=640
    h=480
    currentWindow=Toplevel()
    currentWindow.title("Interactive local structure alignment explorer")
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    currentWindow.attributes('-topmost', 1)
    currentWindow.resizable(False, False)

#    Wybor wzorca
    message="Wzorzec jest struktura, ktora bedziemy probowali dopasowac do czasteczki bazowej.\
    \nWzorzec moze stanowic wycinek czasteczki bazowej, np. jakas struktura drugorzedowa"
    group=LabelFrame(currentWindow,text="Wzorzec",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    Label(group,text=message,anchor=W).pack(fill=BOTH)
    Entry(group,textvariable=templateStructureFile,width=50,state="readonly").pack(pady=5,side=LEFT)
    Button(group,text="Wybierz plik",command=chooseTemplateStructureFile).pack(side=LEFT)
    
#    Wybor pliku mapowania
    group=LabelFrame(currentWindow,text="Plik mapowania",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    Label(group,text="Tutaj wybierz plik mapowania",anchor=W).pack(fill=BOTH)
    Entry(group,textvariable=structureMappingFile,width=50,state="readonly").pack(pady=5,side=LEFT)
    Button(group,text="Wybierz plik",command=chooseStructureMappingFile).pack(side=LEFT)
    
#    Wybor identyfikatora PDB
    group=LabelFrame(currentWindow,text="Identyfikator PDB",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    Label(group,text="Tutaj wybierz plik ",anchor=W).pack(fill=BOTH)
    Entry(group,textvariable=targetStructureFile,width=50,state="readonly").pack(pady=5,side=LEFT)
    Button(group,text="Wybierz plik",command=chooseTargetStructureFile).pack(side=LEFT)
    
    #    ustawianie adresu IP serwera VRPN
    group=LabelFrame(currentWindow,text="Adres IP serwera VRPN",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5)
    Entry(group,justify=CENTER,textvariable=phantomIp,width=30).pack(pady=5,side=LEFT)

#   spacer
    Frame(currentWindow).pack(padx=5,expand=TRUE)
    
#    przyciski
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    Button(group,text="Anuluj",command=currentWindow.destroy).pack(side=RIGHT)
    Button(group,text="Dalej",command=statsWindow).pack()
    
    currentWindow.mainloop();
    
def helloWindow():
    global currentWindow,templateStructureFile,structureMappingFile,phantomIp,targetStructureFile
    
    w=640
    h=480
    currentWindow=Toplevel()
    currentWindow.title("Interactive local structure alignment explorer")
    x=currentWindow.winfo_screenwidth()/2 - w/2
    y=currentWindow.winfo_screenheight()/2 - h/2
    currentWindow.geometry("%dx%d+%d+%d" % (w,h,x,y))
    currentWindow.attributes('-topmost',1)
    currentWindow.resizable(False, False)
    
    helloMsg="\
Dear user.\
\nThis application allows you to interactively explore \
\nprotein and nucleic acids structures. \
\nYou can use this application with Sensable Phantom Omni \
\ndevice and VRPN library.\
\nApplication performs local structure alignment with force \
\nfeedback indicating quality of alignment.\
"
    group=LabelFrame(currentWindow,text="Witaj",padx=5,pady=5)
    group.pack(fill=BOTH,padx=5,pady=5,expand=True)
    Label(group,text=helloMsg).pack(fill=BOTH,side=LEFT)
    dnaImage=PhotoImage(file="dna.gif")
    Label(group,image=dnaImage).pack(fill=BOTH)
    
    group=Frame(currentWindow)
    group.pack(padx=5,pady=5)
    Button(group,text="Cancel",command=currentWindow.destroy).pack(side=RIGHT)
    Button(group,text="NEXT",command=configWindow).pack()
    
#    inicjalizacja zmiennych globalnych    
    templateStructureFile=StringVar(value=os.getcwd()+"/helix_chain_a.pdb")
    structureMappingFile=StringVar(value=os.getcwd()+"/1fg0_helix.map")
    targetStructureFile=StringVar(value=os.getcwd()+"/1fg0.pdb")
    phantomIp=StringVar(value="phantom0@10.21.2.136")
    
    currentWindow.mainloop();
    
    
def __init__(self):
    print "__init__"
    self.menuBar.addmenuitem('Plugin', 'command', 'VRPN',
	label = 'Interactive structure explorer', command = lambda s=self: helloWindow())
                             
