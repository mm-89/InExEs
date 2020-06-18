from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import simulation as sim
from datetime import datetime as dt
import trimesh as tm
import numpy as np
import input_data_handle as idh
import csv
import os
import time
import json
import posture as ps

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("InExES")
        self.minsize(1000,600)
        #self.wm_iconbitmap('blabla.ico') get an icon 


        # FRAMES ---------------------------------------------------
        self.globalFrame = Frame(self, bd= 10, relief = RIDGE, padx = 12)
        self.globalFrame.grid(column = 0, row = 0, sticky='nw')

        self.globalFrame2 = Frame(self, bd= 10, relief = RIDGE, padx = 12)
        self.globalFrame2.grid(column = 1, row = 0, sticky='nw')

        self.meshFrame = LabelFrame(self.globalFrame, text = "Load a mesh")
        self.meshFrame.grid(column = 0, row = 0, pady= 10, sticky='w')
        #self.meshFrame.place(x=30,y=30,height=20,width=100)

        self.dataFrame = LabelFrame(self.globalFrame, text = "Simulation Data")
        self.dataFrame.grid(column = 0, row = 1, pady= 10, sticky='w')

        self.dateFrame = LabelFrame(self.globalFrame, text = "Date and Timestep")
        self.dateFrame.grid(column = 0, row = 2, pady= 10, sticky='w')

        self.outputFrame = LabelFrame(self.globalFrame, text = "Output")
        self.outputFrame.grid(column = 0, row = 3, pady= 10, sticky='w')

        self.colorFrame = LabelFrame(self.globalFrame, text = "Color simulation")
        self.colorFrame.grid(column = 0, row = 4, pady= 10, sticky='w')

        self.startFrame = LabelFrame(self.globalFrame, text = "Start simulation")
        self.startFrame.grid(column = 0, row = 7, pady= 10, sticky='e')

        self.simInfosFrame = LabelFrame(self.globalFrame2, text = "Simulation informations")
        self.simInfosFrame.grid(column = 1, row = 0, padx = 15, sticky='nw')

        # ----------------------------------------------------------


        # WIDGET CREATION ------------------------------------------
        #Button to show mesh in new window
        self.btnShow = Button(self.meshFrame, text="show mesh", bg ="green", command=self.show_mesh)
        
        #Button to show mesh orientation
        self.btnShowOrientation = Button(self.meshFrame, text="show mesh orientation", command=self.reference_frame)

        #Button to show mesh in a precise timestep
        self.btnShowMeshTimestep = Button(self.meshFrame, text = "show mesh in timestep", command = self.show_mesh_in_timestep)

        #Button to start simulation 
        StartBtnImg = PhotoImage(master = self.startFrame ,file='ColorBtn/start.png')
        self.btnStartSimulation = Button(self.startFrame, text = "START SIMULATION", command=self.start_simulation)

        #User input for mesh path
        self.meshName = Entry(self.meshFrame, text = "", bg ="white", width = 20)

        #User input for mesh path
        self.dataName = Entry(self.dataFrame, text = "", bg ="white", width = 20)

        #User input for start date
        self.startDateLabel = Label(self.dateFrame, text = "Start date")
        #User input for end date
        self.endDateLabel = Label(self.dateFrame, text = "End date")
        #User input for timestep
        self.timestepLabel = Label(self.dateFrame,text='Timestep : ')
        self.timestepValue = Entry(self.dateFrame,bg = "white", width = 2)
        self.timestepValue.bind('<KeyRelease>', lambda e: self._check_timestep())

        #User input for output name
        self.ouputLabel = Label(self.outputFrame,text='Output name : ')
        self.ouputValue = Entry(self.outputFrame,bg = "white", width = 20)

        #Color management
        self.color_management()
        # ----------------------------------------------------------

        # SHOW WIDGET INTO THE MAIN WINDOW -------------------------
        self.load_mesh()
        self.load_data()
        #Date picker for start date
        self.start_date_picker(r = 4, col = 2)
        #Date picker for end date
        self.end_date_picker(r = 5, col = 2)
        #Button to show mesh in new window
        self.btnShow.grid(column = 1, row = 2)
        #Button to test mesh orientation
        self.btnShowOrientation.grid(column = 2, row = 2)
        #Button to show mesh in a precise timestep 
        self.btnShowMeshTimestep.grid(column = 3, row = 2)
        #Button to start simulation 
        self.btnStartSimulation.grid(column=1, row=7)
        #User input for mesh path
        self.meshName.grid(column = 2, row = 1)
        #User input for mesh path
        self.dataName.grid(column = 2, row = 3)

        #User input for start date
        self.startDateLabel.grid(column = 1, row = 4)
        #User input for start date
        self.endDateLabel.grid(column = 1, row = 5)
        #User input for timestep
        self.timestepLabel.grid(column = 1, row = 6)
        self.timestepValue.grid(column = 2, row = 6)

        #User input for output value
        self.ouputLabel.grid(column = 1, row = 1)
        self.ouputValue.grid(column = 2, row = 1)

        #Simulation infos
        #self.descriptionStats = Label(self.simInfosFrame, text="Informations for simulations")
        #self.descriptionStats.grid(column=1,row=1)
        self.infos_frame_creation()

        #-----------------------------------------------------------

        #NECESSARY PARAMETERS FOR SIMULATION -----------------------
        self.startDate = ''
        self.endDate = ''
        self.timestep = 0.
        self.mesh = ""
        self.outputName = ""
        self.latitude = 40.
        self.readData = True
        self.dataPath = ""

        #SPECIAL PARAMETERS :
        self.colors = []
        self.preciseTimestep = ''
        #-----------------------------------------------------------

        #TEST BUTTON FUNCTIONS !
        self.tBtn = Button(self, text="test function", command=self.test)
        self.tBtn.grid(column=0, row=8)

        self.autoBtn = Button(self, text="auto complete form", command=self.autocomplete_form)
        self.autoBtn.grid(column=0, row=9)

    def test(self):
        #self.infos_frame_creation()
        #self.make_color_simulation()
        #self.dynamic_color_btn()
        #self.read_json_color()
        self.read_colors_from_ply()
        

    #LOAD MESH FUNCTIONS -------------------------------------------
    def load_mesh(self):
        self.btnMeshLoad = Button(self.meshFrame, text="select a mesh", command = self.file_dialog_mesh)
        self.btnMeshLoad.grid(column = 1, row = 1)

    def file_dialog_mesh(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title = "select a mesh")
        self.meshName.insert(12, self.fileName)
        self.mesh = self.fileName
    #---------------------------------------------------------------

    #LOAD DATA FUNCTIONS -------------------------------------------
    def load_data(self):
        self.btnDataLoad = Button(self.dataFrame, text="select a data file", command = self.file_dialog_data)
        self.btnDataLoad.grid(column = 0, row = 3)

    def file_dialog_data(self):
        self.fileNameData = filedialog.askopenfilename(initialdir = "/", title = "select a data file")
        self.dataName.insert(12, self.fileNameData)
        self.dataPath = self.fileNameData
        self.insert_date_from_data()

    def insert_date_from_data(self):
        allDates = [[]]
        try:

            with open(self.dataPath, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    date = [row["jour"],row["mois"],row["anne"],row["heure"],row["min"],row["sec"]]
                    allDates.append(date)
                    line_count += 1

                #START DATE AUTO INPUT 
                self.entry_1SDay.insert(12, allDates[1][0])
                self.entry_2SDay.insert(12, allDates[1][1])
                self.entry_3SDay.insert(12, allDates[1][2])
                self.entry_4SDay.insert(12, allDates[1][3])
                self.entry_5SDay.insert(12, allDates[1][4])
                self.entry_6SDay.insert(12, allDates[1][5])

                #END DATE AUTO INPUT 
                self.entry_1EDay.insert(12, allDates[-1][0])
                self.entry_2EDay.insert(12, allDates[-1][1])
                self.entry_3EDay.insert(12, allDates[-1][2])
                self.entry_4EDay.insert(12, allDates[-1][3])
                self.entry_5EDay.insert(12, allDates[-1][4])
                self.entry_6EDay.insert(12, allDates[-1][5])

        except IOError:
            self.popupmsg("An error occured : CSV file not found")
    #---------------------------------------------------------------

    #USER INPUT DATE -----------------------------------------------
    def start_date_picker(self, r, col):
        #DATE --> DAY/MONTH/YEAR and HOUR:MIN:SEC START
        self.entry_1SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_1SDay = Label(self.dateFrame, text='MM/')
        self.entry_2SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_2SDay = Label(self.dateFrame, text='DD/')
        self.entry_3SDay = Entry(self.dateFrame, width=4, bg = "white")

        self.entry_4SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_4SDay = Label(self.dateFrame, text='H:')
        self.entry_5SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_5SDay = Label(self.dateFrame, text='M:')
        self.entry_6SDay = Entry(self.dateFrame, width=2, bg = "white")

        self.entry_1SDay.grid(column = col, row = r)
        self.label_1SDay.grid(column = col+1, row = r)
        self.entry_2SDay.grid(column = col+2, row = r)
        self.label_2SDay.grid(column = col+3, row = r)
        self.entry_3SDay.grid(column = col+4, row = r)

        self.entry_4SDay.grid(column = col+5, row = r)
        self.label_4SDay.grid(column = col+6, row = r)
        self.entry_5SDay.grid(column = col+7, row = r)
        self.label_5SDay.grid(column = col+8, row = r)
        self.entry_6SDay.grid(column = col+9, row = r)

        self.entries = [self.entry_1SDay, self.entry_2SDay, self.entry_3SDay, self.entry_4SDay, self.entry_5SDay, self.entry_6SDay]

        self.entry_1SDay.bind('<KeyRelease>', lambda e: self._check(0, 2))
        self.entry_2SDay.bind('<KeyRelease>', lambda e: self._check(1, 2))
        self.entry_3SDay.bind('<KeyRelease>', lambda e: self._check(2, 4))
        self.entry_4SDay.bind('<KeyRelease>', lambda e: self._check(3, 2))
        self.entry_5SDay.bind('<KeyRelease>', lambda e: self._check(4, 2))
        self.entry_6SDay.bind('<KeyRelease>', lambda e: self._check(5, 2))


    def end_date_picker(self, r, col):
        #DATE --> DAY/MONTH/YEAR and HOUR:MIN:SEC END
        self.entry_1EDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_1EDay = Label(self.dateFrame, text='MM/')
        self.entry_2EDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_2EDay = Label(self.dateFrame, text='DD/')
        self.entry_3EDay = Entry(self.dateFrame, width=4, bg = "white")

        self.entry_4EDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_4EDay = Label(self.dateFrame, text='H:')
        self.entry_5EDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_5EDay = Label(self.dateFrame, text='M:')
        self.entry_6EDay = Entry(self.dateFrame, width=2, bg = "white")

        self.entry_1EDay.grid(column = col, row = r)
        self.label_1EDay.grid(column = col+1, row = r)
        self.entry_2EDay.grid(column = col+2, row = r)
        self.label_2EDay.grid(column = col+3, row = r)
        self.entry_3EDay.grid(column = col+4, row = r)

        self.entry_4EDay.grid(column = col+5, row = r)
        self.label_4EDay.grid(column = col+6, row = r)
        self.entry_5EDay.grid(column = col+7, row = r)
        self.label_5EDay.grid(column = col+8, row = r)
        self.entry_6EDay.grid(column = col+9, row = r)

        self.entries2 = [self.entry_1EDay, self.entry_2EDay, self.entry_3EDay, self.entry_4EDay, self.entry_5EDay, self.entry_6EDay]

        self.entry_1EDay.bind('<KeyRelease>', lambda e: self._check2(0, 2))
        self.entry_2EDay.bind('<KeyRelease>', lambda e: self._check2(1, 2))
        self.entry_3EDay.bind('<KeyRelease>', lambda e: self._check2(2, 4))
        self.entry_4EDay.bind('<KeyRelease>', lambda e: self._check2(3, 2))
        self.entry_5EDay.bind('<KeyRelease>', lambda e: self._check2(4, 2))
        self.entry_6EDay.bind('<KeyRelease>', lambda e: self._check2(5, 2))

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, END)
        entry.insert(0, cont[:-1])

    def _check(self, index, size):
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def _check2(self, index, size):
        entry = self.entries2[index]
        next_index = index + 1
        next_entry = self.entries2[next_index] if next_index < len(self.entries2) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def _check_timestep(self):
        entry = self.timestepValue
        data = entry.get()

        if len(data) > 2 or not data.isdigit():
            self._backspace(entry)

    def get_dates_infos(self):
        self.startDate = self.entries[0].get() + '/' + self.entries[1].get() + '/' + self.entries[2].get() + ' ' + self.entries[3].get() + ':' + self.entries[4].get() + ':' + self.entries[5].get()
        self.endDate = self.entries2[0].get() + '/' + self.entries2[1].get() + '/' + self.entries2[2].get() + ' ' + self.entries2[3].get() + ':' + self.entries2[4].get() + ':' + self.entries2[5].get()
        if(self.timestepValue.get() == ''):
            self.popupmsg("Missing timestep !")
        else:
            self.timestep = float(self.timestepValue.get())
    #---------------------------------------------------------------

    #USER INPUT FOR OUTPUT -----------------------------------------
    def get_output_name(self):
        self.outputName = self.ouputValue.get()
    #---------------------------------------------------------------

    #USER INPUT FOR AUTOMATE DATA ----------------------------------
    #---------------------------------------------------------------

    #SHOW MESH AND TESTS MESH FUNCTIONS ----------------------------
    def show_mesh(self):
        if(self.mesh == ""):
            self.popupmsg("Error : Mesh file not found !")
        try :
            meshToShow = tm.load(self.mesh)
            meshToShow.show()
        except IOError:
            self.popupmsg("Error : Mesh file not found !")
        
    
    def reference_frame(self):
        self.error_catch()
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.export_reference_frame()
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")

    def show_mesh_in_timestep(self):
        self.get_dates_infos()
        print(self.startDate)
        self.preciseTimestep = self.startDate
        print(self.preciseTimestep)
        self.error_catch()
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.show_one_timestep(self.preciseTimestep)
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")      


    #---------------------------------------------------------------


    #START SIMULATION ----------------------------------------------
    def start_simulation(self):
        self.get_dates_infos()
        self.get_output_name()
        self.error_catch()
        #Simulation informations/statistics :
        self.infos_frame_creation()
        #self.termf_display()
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.make_simulation()
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")        

    #---------------------------------------------------------------

    #TESTS AND ERRORS USER -----------------------------------------
    def popupmsg(self,msg):
        popup = Tk()
        popup.wm_title("Error found !")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()


    def error_catch(self):
        start = dt.strptime(self.startDate,"%m/%d/%Y %H:%M:%S")
        end = dt.strptime(self.endDate,"%m/%d/%Y %H:%M:%S")
        if(start > end) :
            self.popupmsg("start date is posterior to end date !")

        if(self.timestep == 0. or self.timestep==''):
            self.popupmsg("you need to enter a timestep value !")

        if(self.mesh == ""):
            self.popupmsg("Any mesh selected")

        if(self.outputName == ""):
            self.popupmsg("you need to enter a output name !")

        if(self.readData == True and self.dataPath == ""):
            self.popupmsg("You choose to use a data file, but no file selected !")

        if(self.readData == False and self.latitude == ""):
            self.popupmsg("You choose to generate data automatically, but no latitude value found !")
        
        try :
            file = open(self.dataPath,'r')
        except IOError:
            self.popupmsg("Error : Data file not found !")
        try :
            file = open(self.mesh,'r')
        except IOError:
            self.popupmsg("Error : Mesh file not found !")


    def infos_frame_creation(self):
        '''tmpMesh = self.mesh.split('/')
        tmpData = self.dataPath.split('/') 
        cutMeshName = tmpMesh[-1]
        cutDataName = tmpData[-1]'''
        self.betaLoadingLabel = Label(self.simInfosFrame, text="Beta coefficient : ")
        self.simLoadingLabel = Label(self.simInfosFrame, text="Simulation : ")

        self.infoNameMesh = Label(self.simInfosFrame, text="Mesh : ")
        self.infoNameData = Label(self.simInfosFrame, text="Data file used : ")
        self.infoStartDate = Label(self.simInfosFrame, text="Start date : ")
        self.infoEndDate = Label(self.simInfosFrame, text="End date : ")
        self.infoTimestep = Label(self.simInfosFrame, text="Timestep : ")
        self.infoOutput = Label(self.simInfosFrame, text="Output file : output/")

        self.betaLoadingLabel.grid(column=1, row=3)
        self.betaLoadingLabel.grid(column=1, row=4)

        self.betaLoadingLabel.grid(column=1, row=5)
        self.betaLoadingLabel.grid(column=1, row=6)
        self.betaLoadingLabel.grid(column=1, row=7)
        self.betaLoadingLabel.grid(column=1, row=8)
        self.betaLoadingLabel.grid(column=1, row=9)
        self.betaLoadingLabel.grid(column=1, row=10)

    def autocomplete_form(self):
        self.dataPath = "/Users/osvaldo/Projet_dev/PYTHON/inexes/InExEs/input/irradiance_2009.csv"
        self.mesh = "/Users/osvaldo/Projet_dev/PYTHON/inexes/InExEs/postures/cube.ply"
        self.meshName.insert(12, "/Users/osvaldo/Projet_dev/PYTHON/inexes/InExEs/postures/cube.ply")
        self.insert_date_from_data()
        self.timestepValue.insert(12, '60')
        self.ouputValue.insert(12, 'test')
        self.dataName.insert(12, "/Users/osvaldo/Projet_dev/PYTHON/inexes/InExEs/input/irradiance_2009.csv")
        self.outputName = 'test'

    #---------------------------------------------------------------

    #COLORS MANAGEMENT -----------------------------------------
    def colors_popup(self):
        self.popupColor = Tk()
        self.popupColor.wm_title("Choose the color to simulate")
        #Colors :
        Red = PhotoImage(master = self.popupColor ,file='ColorBtn/Red.png')
        Blue = PhotoImage(master = self.popupColor ,file='ColorBtn/Blue.png')
        # Color button list :
        redBtn = Button(self.popupColor, image =Red, command = lambda : self.input_choosed_color("RED"), height = 40, width = 100  )
        blueBtn = Button(self.popupColor, image =Blue, command = lambda : self.input_choosed_color("BLUE"), height = 40, width = 100 )
        #Color button placement :
        redBtn.grid(column = 0, row = 0)
        blueBtn.grid(column = 0, row = 1)

        #Close button
        closeColorBtn = Button(self.popupColor, text = "Close", command = self.popupColor.destroy)
        closeColorBtn.grid(column = 0, row = 2, padx = 5)
        self.popupColor.mainloop()

    def color_management(self):
        self.colorInput = Entry(self.colorFrame, width=10, bg = "white")
        self.colorInput.grid(column = 0, row = 0)

        self.chooseColorBtn = Button(self.colorFrame, text="Choose a color", command = self.dynamic_color_btn)
        self.chooseColorBtn.grid(column = 1, row = 0, padx = 4)


    def input_choosed_color(self, color):
        self.colorInput.insert(12, color+',')
        #self.popupColor.destroy()

    def make_color_simulation(self):
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.set_zone_to_simulate("red")
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...") 

    def color_verification(self, color):
        check = any
        

    def dynamic_color_btn(self):
        #self.read_json_color()
        self.read_colors_from_ply()
        self.colorPopup = Tk()
        self.colorPopup.wm_title("Choose the color to simulate")
        self.colorPopup.minsize(600,400)
        col = 0
        r = 0
        for i in range(100):
            
            newButton = Button(self.colorPopup, text=str(i+1)+': '+ self.colors[i], fg =self.colors[i],
                        command=lambda j=i+1: self.input_choosed_color(self.colors[j-1]))

            if((i+1)%10 == 0):
                newButton.grid(column = col, row = r)
                col = 0
                r = r + 1
            else:
                newButton.grid(column = col, row = r)
                col += 1

        self.colorSaveBtn = Button(self.colorPopup, text="Validate color(s)", command= print(self.colorInput.get()))
        self.colorSaveBtn.grid()

    def read_json_color(self):
        with open('ColorBtn/colors.json') as json_file:
            data = json.load(json_file)
            print(type(data[0]['rgb']))
            for c in data:
                print('HEX code: ' + c['hexString'])
                self.colors.append(c['hexString'])
                for key, value in c['rgb'].items():
                    print (key, value)
                print('Name: ' + c['name'])
                print('')

    def read_colors_from_ply(self):
        print("Reading PLY colors :")

        rgbColors = [[]]

        try:
            self.posture = ps.Posture('postures/body_low_res/BabyLowRes_01.ply')
        except IOError:
            self.popupmsg("You need to choose a valid mesh before !") 

        for k, item in enumerate(self.posture.get_faces_color):
            rgbColors.append(item)

        rgbColorsSet = set(tuple(i) for i in rgbColors)

        print("list size : ", len(rgbColors), "set size : ", len(rgbColorsSet))
        self.rgb_to_hex(rgbColorsSet)


    def rgb_to_hex(self, rgb):
        self.colorsDict = {}
        rgb.pop()
        for c in rgb:
            cpyC = list(c)
            if not cpyC:
                print("empty list")
            else:
                hexColor = '#{:02x}{:02x}{:02x}'.format(cpyC[0],cpyC[1],cpyC[2])
                self.colors.append(hexColor)
                self.colorsDict.update({hexColor:cpyC})



        






        




