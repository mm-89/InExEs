from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import simulation as sim
from datetime import datetime as dt
import trimesh as tm


class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("InExES")
        self.minsize(640,400)
        #self.wm_iconbitmap('blabla.ico') get an icon 


        # FRAMES ---------------------------------------------------
        self.meshFrame = LabelFrame(self, text = "Load a mesh")
        self.meshFrame.grid(column = 0, row = 0)

        self.dataFrame = LabelFrame(self, text = "Simulation Data")
        self.dataFrame.grid(column = 0, row = 1)

        self.dateFrame = LabelFrame(self, text = "Date and Timestep")
        self.dateFrame.grid(column = 0, row = 2)

        self.outputFrame = LabelFrame(self, text = "Output")
        self.outputFrame.grid(column = 0, row = 3)

        self.startFrame = LabelFrame(self, text = "Start simulation")
        self.startFrame.grid(column = 0, row = 7)
        # ----------------------------------------------------------


        # WIDGET CREATION ------------------------------------------
        #Button to show mesh in new window
        self.btnShow = Button(self.meshFrame, text="show mesh", bg ="green", command=self.show_mesh)

        #Button to start simulation 
        self.btnStartSimulation = Button(self.startFrame, text="start simualation", bg ="green", command=self.start_simulation)

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
        # ----------------------------------------------------------

        # SHOW WIDGET INTO THE MAIN WINDOW -------------------------
        self.load_mesh()
        self.load_data()
        #Date picker for start date
        self.start_date_picker(r = 4, col = 2)
        #Date picker for end date
        self.end_date_picker(r = 5, col = 2)
        #Button to show mesh in new window
        self.btnShow.grid(column=1, row=0)
        #Button to start simulation 
        self.btnStartSimulation.grid(column=1, row=7)
        #User input for mesh path
        self.meshName.grid(column = 2, row = 2)
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

    def test(self):
        self.get_dates_infos()
        self.get_output_name()
        print("mesh : " , self.mesh)
        print("data file : ", self.dataPath)
        print("start infos : " , self.startDate)
        print("end infos : " , self.endDate)
        print("timestep infos : " , self.timestep)
        print("output name : " , self.outputName)
        print(type(self.timestep))

    #LOAD MESH FUNCTIONS -------------------------------------------
    def load_mesh(self):
        self.btnMeshLoad = Button(self.meshFrame, text="select a mesh", command = self.file_dialog_mesh)
        self.btnMeshLoad.grid(column = 1, row = 2)

    def file_dialog_mesh(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title = "select a mesh")
        self.meshName.insert(12, self.fileName)
        self.mesh = self.fileName
    #---------------------------------------------------------------

    #LOAD DATA FUNCTIONS -------------------------------------------
    def load_data(self):
        self.btnDataLoad = Button(self.dataFrame, text="select a data file", command = self.file_dialog_data)
        self.btnDataLoad.grid(column = 1, row = 3)

    def file_dialog_data(self):
        self.fileNameData = filedialog.askopenfilename(initialdir = "/", title = "select a data file")
        self.dataName.insert(12, self.fileNameData)
        self.dataPath = self.fileNameData
    #---------------------------------------------------------------

    #USER INPUT DATE -----------------------------------------------
    def start_date_picker(self, r, col):
        #DATE --> DAY/MONTH/YEAR and HOUR:MIN:SEC START
        self.entry_1SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_1SDay = Label(self.dateFrame, text='DD/')
        self.entry_2SDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_2SDay = Label(self.dateFrame, text='MM/')
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
        self.label_1EDay = Label(self.dateFrame, text='DD/')
        self.entry_2EDay = Entry(self.dateFrame, width=2, bg = "white")
        self.label_2EDay = Label(self.dateFrame, text='MM/')
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
        if(self.mesh == ""):
            self.popupmsg("Error : Mesh file not found !")
        try :
            simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
            simulation.export_reference_frame()
        except IOError:
            self.popupmsg("An error occured ! Please verify simulation parameters...")

    def show_mesh_in_timestep(self):
        if(self.mesh == ""):
            self.popupmsg("Error : Mesh file not found !")
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
        simulation = sim.Simulation(self.startDate,self.endDate,self.timestep,self.mesh,self.outputName,self.latitude,self.readData,self.dataPath)
        simulation.make_simulation()
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
        start = dt.strptime(self.startDate,"%d/%m/%Y %H:%M:%S")
        end = dt.strptime(self.endDate,"%d/%m/%Y %H:%M:%S")
        if(start > end) :
            self.popupmsg("start date is posterior to end date !")

        if(self.timestep == 0.):
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



