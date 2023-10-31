from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import simulation as sim
import posture as ps
import csvReader as cr

from datetime import datetime as dt
import trimesh as tm
import numpy as np
import csv
import os
import time
import json
import re

curr_dir = os.getcwd()

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("InExES")
        self.minsize(1000,600)

        #MICHELE
        #can be interesting ---------------
        #width = self.winfo_screenwidth()
        #height = self.winfo_screenheight()

        #top = self.winfo_toplevel()
        #top.rowconfigure(0, weight=1)
        #top.columnconfigure(0, weight=1)  

        #self.wm_iconbitmap('blabla.ico') get an icon 
        #----------------------------------

        #GLOBAL FRAMES ---------------------------------------------------
        self.globalFrame = Frame(self, bd= 10,relief = RIDGE, padx = 12)
        self.globalFrame.grid(column = 0, row = 0, sticky='nw')

        self.globalFrame2 = Frame(self, bd= 10, relief = RIDGE, padx = 12)
        self.globalFrame2.grid(column = 1, row = 0, sticky='nw')

        self.globalFrame3 = Frame(self, bd= 10, relief = RIDGE, padx = 12)
        self.globalFrame3.grid(column = 0, row = 1, sticky='nw')

        #----------------------------------------------------------- 

        self.meshFrame = LabelFrame(self.globalFrame, text = "Load a mesh")
        self.meshFrame.grid(column = 0, row = 0, pady= 10, sticky='w')
        #self.meshFrame.place(x=30,y=30,height=20,width=100)

        self.dataFrame = LabelFrame(self.globalFrame, text = "Simulation Data")
        self.dataFrame.grid(column = 0, row = 1, pady= 10, sticky='w')

        self.dateFrame = LabelFrame(self.globalFrame, text = "Date")
        self.dateFrame.grid(column = 0, row = 2, pady= 10, sticky='w')

        self.timestepFrame = LabelFrame(self.globalFrame, text = "Simulation timestep")
        self.timestepFrame.grid(column = 0, row = 3, pady= 10, sticky='w')

        self.outputFrame = LabelFrame(self.globalFrame, text = "Output")
        self.outputFrame.grid(column = 0, row = 4, pady= 10, sticky='w')

        self.colorFrame = LabelFrame(self.globalFrame, text = "Color simulation")
        self.colorFrame.grid(column = 0, row = 5, pady= 10, sticky='w')

        self.startFrame = LabelFrame(self.globalFrame, text = "Start simulation")
        self.startFrame.grid(column = 0, row = 8, pady= 10, sticky='e')

        self.simInfosFrame = LabelFrame(self.globalFrame2, text = "Simulation informations")
        self.simInfosFrame.grid(column = 1, row = 0, padx = 15, sticky='nw')

        self.commandsFrame = LabelFrame(self.globalFrame3, text = "Others commands")
        self.commandsFrame.grid(column = 1, row = 0, padx = 15, sticky='w')

        # ----------------------------------------------------------


        # WIDGET CREATION ------------------------------------------
        #Button to show mesh in new window
        self.btnShow = Button(self.meshFrame, text="show mesh", command=self.show_mesh)
        
        #Button to show mesh orientation
        self.btnShowOrientation = Button(self.meshFrame, text="export reference frame", command=self.reference_frame)

        #Button to show mesh in a precise timestep
        self.btnShowMeshTimestep = Button(self.meshFrame, text = "show mesh in one timestep exposition", command = self.timestep_selector)

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
        self.timestepLabel = Label(self.timestepFrame,text='Timestep : ')
        self.timestepValue = Entry(self.timestepFrame,bg = "white", width = 10,
                                    textvariable=StringVar(self.dateFrame, 
                                            value='60.'))
        self.timestepValue.bind('<KeyRelease>', lambda e: self._check_timestep())

        #User input for output name
        self.ouputLabel = Label(self.outputFrame,text='Output name : ')
        self.ouputValue = Entry(self.outputFrame,bg = "white", width = 20)

        #Color management
        self.color_management()
        # ----------------------------------------------------------

        #MICHELE - new date to show --------........................
        month_txt = Label(self.dateFrame, text='mm')
        month_txt.grid(column = 3, row = 5)

        day_txt = Label(self.dateFrame, text='dd')
        day_txt.grid(column = 4, row = 5)

        year_txt = Label(self.dateFrame, text='yyyy')
        year_txt.grid(column = 5, row = 5)

        pause_txt = Label(self.dateFrame, text=' ')
        pause_txt.grid(column = 6, row = 5)

        hour_txt = Label(self.dateFrame, text='h')
        hour_txt.grid(column = 8, row = 5)

        month_txt = Label(self.dateFrame, text='m')
        month_txt.grid(column = 9, row = 5)

        second_txt = Label(self.dateFrame, text='s')
        second_txt.grid(column = 10, row = 5)

        # SHOW WIDGET INTO THE MAIN WINDOW -------------------------
        self.load_mesh()
        self.load_data()
        #Date picker for start date
        self.start_date_picker(r = 6, col = 2)
        #Date picker for end date
        self.end_date_picker(r = 7, col = 2)
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
        self.startDateLabel.grid(column = 1, row = 6)
        #User input for start date
        self.endDateLabel.grid(column = 1, row = 7)
        #User input for timestep
        self.timestepLabel.grid(column = 1, row = 8)
        self.timestepValue.grid(column = 2, row = 8)

        #User input for output value
        self.ouputLabel.grid(column = 1, row = 1)
        self.ouputValue.grid(column = 2, row = 1)

        #Simulation infos
        #self.descriptionStats = Label(self.simInfosFrame, text="Informations for simulations")
        #self.descriptionStats.grid(column=1,row=1)
        #self.infos_frame_creation()

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
        self.inProgress = 'in progress'
        self.done = 'done'
        self.hexString = ''

        #-----------------------------------------------------------

        #TEST BUTTON FUNCTIONS !
        self.tBtn = Button(self, text="test function", command=self.test)
        self.tBtn.grid(column=0, row=8)

        self.autoBtn = Button(self.globalFrame3, text="auto complete form", command=self.autocomplete_form)
        self.autoBtn.grid(column=1, row=1)

        self.autoCompleteBtn = Button(self.globalFrame3, text="auto complete with last form", command=self.autocomplete_with_saved_form)
        self.autoCompleteBtn.grid(column=1, row=2)

        self.clearAllBtn = Button(self.globalFrame3, text="clear form", command=self.clear_all)
        self.clearAllBtn.grid(column=1, row=3)

    def test(self):
        self.timestep_selector()
        

    #LOAD MESH FUNCTIONS -------------------------------------------
    def load_mesh(self):
        self.btnMeshLoad = Button(self.meshFrame, text="select a mesh", command = self.file_dialog_mesh)
        self.btnMeshLoad.grid(column = 1, row = 1)

    def file_dialog_mesh(self):
        self.fileName = filedialog.askopenfilename(initialdir = curr_dir + "/postures", title = "select a mesh")
        self.meshName.insert(12, self.fileName)
        self.mesh = self.fileName
    #---------------------------------------------------------------

    #LOAD DATA FUNCTIONS -------------------------------------------
    def load_data(self):
        self.btnDataLoad = Button(self.dataFrame, text="select a data file", command = self.file_dialog_data)
        self.btnDataLoad.grid(column = 0, row = 3)

    def file_dialog_data(self):
        self.fileNameData = filedialog.askopenfilename(initialdir = curr_dir + "/input_irradiance", title = "select a data file")
        self.dataName.insert(12, self.fileNameData)
        self.dataPath = self.fileNameData
        self.insert_date_from_data()

    def insert_date_from_data(self):
        
        curr_input = cr.CsvReader(self.dataPath)

        first_data = dt.strptime(curr_input.datetime[0], "%b %d %Y %H:%M:%S")
        last_data = dt.strptime(curr_input.datetime[-1], "%b %d %Y %H:%M:%S")

        #START DATE AUTO INPUT 
        self.entry_1SDay.insert(12, first_data.month)
        self.entry_2SDay.insert(12, first_data.day)
        self.entry_3SDay.insert(12, first_data.year)
        self.entry_4SDay.insert(12, first_data.hour)
        self.entry_5SDay.insert(12, first_data.minute)
        self.entry_6SDay.insert(12, first_data.second)

        #END DATE AUTO INPUT 
        self.entry_1EDay.insert(12, last_data.month)
        self.entry_2EDay.insert(12, last_data.day)
        self.entry_3EDay.insert(12, last_data.year)
        self.entry_4EDay.insert(12, last_data.hour)
        self.entry_5EDay.insert(12, last_data.minute)
        self.entry_6EDay.insert(12, last_data.second)
    #---------------------------------------------------------------

    #USER INPUT DATE -----------------------------------------------
    def start_date_picker(self, r, col):
        #DATE --> MONTH/DAY/YEAR and HOUR:MIN:SEC START
        # plus old labels
        self.entry_1SDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_1SDay = Label(self.dateFrame, text='MM/')
        self.entry_2SDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_2SDay = Label(self.dateFrame, text='DD/')
        self.entry_3SDay = Entry(self.dateFrame, width=4, bg = "white")

        self.entry_4SDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_4SDay = Label(self.dateFrame, text='H:')
        self.entry_5SDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_5SDay = Label(self.dateFrame, text='M:')
        self.entry_6SDay = Entry(self.dateFrame, width=2, bg = "white")

        self.entry_1SDay.grid(column = col+1, row = r)
        #self.label_1SDay.grid(column = col+1, row = r)
        self.entry_2SDay.grid(column = col+2, row = r)
        #self.label_2SDay.grid(column = col+3, row = r)
        self.entry_3SDay.grid(column = col+3, row = r)

        self.entry_4SDay.grid(column = col+6, row = r)
        #self.label_4SDay.grid(column = col+6, row = r)
        self.entry_5SDay.grid(column = col+7, row = r)
        #self.label_5SDay.grid(column = col+8, row = r)
        self.entry_6SDay.grid(column = col+8, row = r)

        self.entries = [self.entry_1SDay, self.entry_2SDay, self.entry_3SDay, self.entry_4SDay, self.entry_5SDay, self.entry_6SDay]

        self.entry_1SDay.bind('<KeyRelease>', lambda e: self._check(0, 2))
        self.entry_2SDay.bind('<KeyRelease>', lambda e: self._check(1, 2))
        self.entry_3SDay.bind('<KeyRelease>', lambda e: self._check(2, 4))
        self.entry_4SDay.bind('<KeyRelease>', lambda e: self._check(3, 2))
        self.entry_5SDay.bind('<KeyRelease>', lambda e: self._check(4, 2))
        self.entry_6SDay.bind('<KeyRelease>', lambda e: self._check(5, 2))


    def end_date_picker(self, r, col):
        #DATE --> MONTH/DAY/YEAR and HOUR:MIN:SEC END
        # plus, old labels
        self.entry_1EDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_1EDay = Label(self.dateFrame, text='MM/')
        self.entry_2EDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_2EDay = Label(self.dateFrame, text='DD/')
        self.entry_3EDay = Entry(self.dateFrame, width=4, bg = "white")

        self.entry_4EDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_4EDay = Label(self.dateFrame, text='H:')
        self.entry_5EDay = Entry(self.dateFrame, width=2, bg = "white")
        #self.label_5EDay = Label(self.dateFrame, text='M:')
        self.entry_6EDay = Entry(self.dateFrame, width=2, bg = "white")

        self.entry_1EDay.grid(column = col+1, row = r)
        #self.label_1EDay.grid(column = col+1, row = r)
        self.entry_2EDay.grid(column = col+2, row = r)
        #self.label_2EDay.grid(column = col+3, row = r)
        self.entry_3EDay.grid(column = col+3, row = r)

        self.entry_4EDay.grid(column = col+6, row = r)
        #self.label_4EDay.grid(column = col+6, row = r)
        self.entry_5EDay.grid(column = col+7, row = r)
        #self.label_5EDay.grid(column = col+8, row = r)
        self.entry_6EDay.grid(column = col+8, row = r)

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
        self.startDate = self.entries[0].get() + \
                    '/' + self.entries[1].get() + \
                    '/' + self.entries[2].get() + \
                    ' ' + self.entries[3].get() + \
                    ':' + self.entries[4].get() + \
                    ':' + self.entries[5].get()
        self.endDate = self.entries2[0].get() + \
                    '/' + self.entries2[1].get() + \
                    '/' + self.entries2[2].get() + \
                    ' ' + self.entries2[3].get() + \
                    ':' + self.entries2[4].get() + \
                    ':' + self.entries2[5].get()
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
            return
        
    
    def reference_frame(self):
        self.get_dates_infos()
        self.get_output_name()
        self.error_catch()
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.export_reference_frame()
        except (IOError, ValueError) as e:
            self.popupmsg("An error occured ! Please verify simulation parameters...")

    def show_mesh_in_timestep(self):
        selectedTimestep = self.get_date_timestep_selector()
        if(selectedTimestep == ''):
            self.popupmsg("You need to choose a timestep !")

        self.get_dates_infos()
        self.get_output_name()
        self.error_catch()
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.show_one_timestep(selectedTimestep)
        except (IOError) as e:
            self.popupmsg("An error occured ! Please verify parameters...")      


    def timestep_selector(self):
        if(self.mesh == ""):
            self.popupmsg("You need to select a mesh before !")
            return
        self.timestepSelector = Tk()
        self.timestepSelector.wm_title("Please select a timestep")

        self.timestepE1 = Entry(self.timestepSelector, width=2, bg = "white")
        self.labelE1 = Label(self.timestepSelector, text='MM/')
        self.timestepE2 = Entry(self.timestepSelector, width=2, bg = "white")
        self.labelE2 = Label(self.timestepSelector, text='DD/')
        self.timestepE3 = Entry(self.timestepSelector, width=4, bg = "white")

        self.timestepE4 = Entry(self.timestepSelector, width=2, bg = "white")
        self.labelE4 = Label(self.timestepSelector, text='H:')
        self.timestepE5 = Entry(self.timestepSelector, width=2, bg = "white")
        self.labelE5 = Label(self.timestepSelector, text='M:')
        self.timestepE6 = Entry(self.timestepSelector, width=2, bg = "white")

        self.timestepE1.grid(column = 0, row = 1)
        self.labelE1.grid(column = 1, row = 1)
        self.timestepE2.grid(column = 2, row = 1)
        self.labelE2.grid(column = 3, row = 1)
        self.timestepE3.grid(column = 4, row = 1)

        self.timestepE4.grid(column = 5, row = 1)
        self.labelE4.grid(column = 6, row = 1)
        self.timestepE5.grid(column = 7, row = 1)
        self.labelE5.grid(column = 8, row = 1)
        self.timestepE6.grid(column = 9, row = 1)

        self.timestepSelectorEntries = [self.timestepE1, self.timestepE2, self.timestepE3, self.timestepE4, self.timestepE5, self.timestepE6]

        self.timestepE1.bind('<KeyRelease>', lambda e: self._check3(0, 2))
        self.timestepE2.bind('<KeyRelease>', lambda e: self._check3(1, 2))
        self.timestepE3.bind('<KeyRelease>', lambda e: self._check3(2, 4))
        self.timestepE4.bind('<KeyRelease>', lambda e: self._check3(3, 2))
        self.timestepE5.bind('<KeyRelease>', lambda e: self._check3(4, 2))
        self.timestepE6.bind('<KeyRelease>', lambda e: self._check3(5, 2))
        B1 = Button(self.timestepSelector, text="Proceed", command = self.show_mesh_in_timestep)
        B1.grid()
        self.timestepSelector.update()


    def _check3(self, index, size):
        entry = self.timestepSelectorEntries[index]
        next_index = index + 1
        next_entry = self.timestepSelectorEntries[next_index] if next_index < len(self.timestepSelectorEntries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()


    def get_date_timestep_selector(self):
        return self.timestepSelectorEntries[0].get() + '/' + self.timestepSelectorEntries[1].get() + '/' + self.timestepSelectorEntries[2].get() + ' ' + self.timestepSelectorEntries[3].get() + ':' + self.timestepSelectorEntries[4].get() + ':' + self.timestepSelectorEntries[5].get() 
    
    #---------------------------------------------------------------


    #START SIMULATION ----------------------------------------------
    def start_simulation(self):
        self.get_dates_infos()
        self.get_output_name()
        self.error_catch()
        #Simulation informations/statistics :
        self.infos_frame_creation()
        #self.termf_display()
        #save form
        self.save_form()
        try:
            self.curr_simulation = sim.Simulation(self.startDate,
                                        self.endDate,
                                        self.timestep,
                                        self.mesh,
                                        self.outputName,
                                        self.latitude,
                                        self.readData,
                                        self.dataPath)
            self.betaLoadingLabel['text'] = "Beta coefficient : " + self.done

        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")

        if(self.colorInput.get() != ''):
            print("Color simulation possible")
            self.make_color_simulation()
        
        try:      
            self.curr_simulation.make_simulation()
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")
            

        self.simLoadingLabel['text'] = "Simulation : " + self.done
        self.simInfosFrame.update()

    #---------------------------------------------------------------

    #TESTS AND ERRORS USER -----------------------------------------
    def popupmsg(self,msg):
        popup = Tk()
        popup.wm_title("Error found !")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.update()


    def error_catch(self):
        try:
            start = dt.strptime(self.startDate,"%m/%d/%Y %H:%M:%S")
            end = dt.strptime(self.endDate,"%m/%d/%Y %H:%M:%S")
        except ValueError:
            self.popupmsg("An error occured : Missing start and end")
        if(start > end) :
            self.popupmsg("start date is posterior to end date !")

        if(self.timestep == 0. or self.timestep==''):
            self.popupmsg("you need to enter a timestep value !")

        if(self.mesh == ""):
            self.popupmsg("Any mesh selected")

        if(self.outputName == ""):
            self.popupmsg("you need to enter a output name !")

        try :
            file = open(self.dataPath,'r')
        except IOError:
            self.popupmsg("Error : Data file not found !")
        try :
            file = open(self.mesh,'r')
        except IOError:
            self.popupmsg("Error : Mesh file not found !")


    def infos_frame_creation(self):
        tmpMesh = self.mesh.split('/')
        tmpData = self.dataPath.split('/') 
        cutMeshName = tmpMesh[-1]
        cutDataName = tmpData[-1]
        self.betaLoadingLabel = Label(self.simInfosFrame, text="Beta coefficient : " + self.inProgress  ,font = "TkDefaultFont 14 bold")
        self.simLoadingLabel = Label(self.simInfosFrame, text="Simulation : " + self.inProgress,font = "TkDefaultFont 14 bold")

        self.infoNameMesh = Label(self.simInfosFrame, text="Mesh : " + cutMeshName,font = "TkDefaultFont 14 bold")
        self.infoNameData = Label(self.simInfosFrame, text="Data file used : " + cutDataName,font = "TkDefaultFont 14 bold")
        self.infoStartDate = Label(self.simInfosFrame, text="Start date : " + self.startDate,font = "TkDefaultFont 14 bold")
        self.infoEndDate = Label(self.simInfosFrame, text="End date : " + self.endDate,font = "TkDefaultFont 14 bold")
        self.infoTimestep = Label(self.simInfosFrame, text="Timestep : " + str(self.timestep),font = "TkDefaultFont 14 bold")
        self.infoOutput = Label(self.simInfosFrame, text="Output file : output/" + self.outputName,font = "TkDefaultFont 14 bold")

        self.betaLoadingLabel.grid(column=1, row=3)
        self.simLoadingLabel.grid(column=1, row=4)

        self.infoNameMesh.grid(column=1, row=5)
        self.infoNameData.grid(column=1, row=6)
        self.infoStartDate.grid(column=1, row=7)
        self.infoEndDate.grid(column=1, row=8)
        self.infoTimestep.grid(column=1, row=9)
        self.infoOutput.grid(column=1, row=10)

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


    def input_choosed_color(self, color,index):
        self.hexString += color+','
        self.colorInput.insert(12, color+',')
        self.buttons[index].config(state="disabled")
        #self.popupColor.destroy()

    def validate_colors(self):
        #hexList = self.colorInput.get().split(',')
        hexList = self.hexString.split(',')
        hexList.pop() #get rid of last element because it' always empty
        self.rgbList = []
        
        for c in hexList:
            self.rgbList.append(self.colorsDict.get(c))
        
        self.colorPopup.destroy()
        #Making sure there the same color twice
        tmp = set(tuple(x) for x in self.rgbList)
        self.rgbMap = list(tmp)
        print(self.rgbList)
        print(self.rgbMap)
        self.addColors = []
        for c in self.rgbList:
            self.addColors += c

    def make_color_simulation(self):
        try :
            #simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath,loop_on_faces=True)
            self.curr_simulation.set_zone_to_simulate(self.addColors)
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...") 

    def color_verification(self, color):
        check = any
        

    def dynamic_color_btn(self):
        self.colors = []
        self.read_colors_from_ply()
        self.colorPopup = Tk()
        self.colorPopup.wm_title("Choose the color to simulate")
        self.colorPopup.minsize(600,400)
        col = 0
        r = 0
        self.buttons = []
        for i in range(len(self.colors)):
            newButton = Button(self.colorPopup, text=str(i+1)+': '+ self.colors[i], fg =self.colors[i],
                        command=lambda j=i+1: self.input_choosed_color(self.colors[j-1], j-1))

            if((i+1)%10 == 0):
                newButton.grid(column = col, row = r)
                col = 0
                r = r + 1
            else:
                newButton.grid(column = col, row = r)
                col += 1

            self.buttons.append(newButton)
        self.colorSaveBtn = Button(self.colorPopup, text="Validate color(s)", command= self.validate_colors)
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
        if(self.mesh == ''):
            self.popupmsg("Mesh not found")
        else:
            try:
                self.posture = ps.Posture(self.mesh)
            except ValueError:
                self.popupmsg("Mesh not found") 
                return

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
                if(hexColor is not None):
                    self.colors.append(hexColor)
                    self.colorsDict.update({hexColor:cpyC})

 #---------------------------------------------------------------

    #SAVE AND AUTO COMPLETE FORM -----------------------------------------

    def autocomplete_form(self):
        #self.mesh = curr_dir + "postures/cube.ply"
        #self.meshName.insert(12, "/Users/osvaldo/Projet_dev/PYTHON/inexes/InExEs/postures/cube.ply")
        self.dataPath = "{}/input_irradiance/irradiance_2009.csv".format(curr_dir)
        self.insert_date_from_data()
        #self.timestepValue.insert(12, '60.')
        #self.ouputValue.insert(12, 'test')
        self.dataName.insert(12, "{}/input_irradiance/irradiance_2009.csv".format(curr_dir))
        #self.outputName = 'test'

    def save_form(self):
        self.saveMesh = self.mesh
        self.saveData = self.dataPath
        self.saveStart = self.startDate
        self.saveEnd = self.endDate
        self.saveTimestep = self.timestep
        self.saveOutput = self.outputName

    def autocomplete_with_saved_form(self):
        self.meshName.insert(12,self.saveMesh)
        self.dataName.insert(12,self.saveData)
        self.timestepValue.insert(12,self.saveTimestep)
        self.ouputValue.insert(12,self.saveOutput)
        #Insert dates
        #START DATE AUTO INPUT 
        startList = re.split('/| |:',self.saveStart)
        endList = re.split('/| |:',self.saveEnd)
        self.entry_1SDay.insert(12, startList[0])
        self.entry_2SDay.insert(12, startList[1])
        self.entry_3SDay.insert(12, startList[2])
        self.entry_4SDay.insert(12, startList[3])
        self.entry_5SDay.insert(12, startList[4])
        self.entry_6SDay.insert(12, startList[5])

        #END DATE AUTO INPUT 
        self.entry_1EDay.insert(12, endList[0])
        self.entry_2EDay.insert(12, endList[1])
        self.entry_3EDay.insert(12, endList[2])
        self.entry_4EDay.insert(12, endList[3])
        self.entry_5EDay.insert(12, endList[4])
        self.entry_6EDay.insert(12, endList[5])

    def clear_all(self):
        widget_list = self.all_children()
        for item in widget_list:
            if(isinstance(item, Entry)):
                item.delete(0,'end')


    def all_children (self) :
        _list = self.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list



        






        




