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
        # ----------------------------------------------------------


        # WIDGET CREATION ------------------------------------------
        self.labelFrame = ttk.LabelFrame(self, text = "Open a file")
        self.labelFrame.grid(column = 0, row = 2)

        btnShow = Button(self, text="show mesh", bg ="green", command=self.show_mesh)
        btnStartSimulation = Button(self, text="start simualation", bg ="green", command=self.start_simulation)

        
        # ----------------------------------------------------------

        #NECESSARY PARAMETERS FOR SIMULATION -----------------------
        self.startDate = '05/01/2009 00:01:00'
        self.endDate = '05/02/2009 00:01:00'
        self.timestep = 60.
        self.mesh = ""
        self.outputName = "face_may_with"
        self.latitude = 40.
        self.readData = True
        self.dataPath = "input/irradiance_2009.csv"
        #-----------------------------------------------------------

        # SHOW WIDGET INTO THE MAIN WINDOW -------------------------
        self.load_mesh()
        #Button to show mesh in new window
        btnShow.grid(column=1, row=0)
        #Button to start simulation 
        btnStartSimulation.grid(column=0, row=0)
        #-----------------------------------------------------------

    #LOAD MESH FUNCTIONS -------------------------------------------
    def load_mesh(self):
        self.btnMeshLoad = ttk.Button(self.labelFrame, text="browse a file", command = self.fileDialog)
        self.btnMeshLoad.grid(column = 1, row = 2)

    def fileDialog(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title = "select a mesh")
        self.meshName = ttk.Label(self.labelFrame, text = "")
        self.meshName.grid(column = 2, row = 2)
        self.meshName.configure(text = self.fileName)
        self.mesh = self.fileName
    #---------------------------------------------------------------

    #LOAD DATA FUNCTIONS -------------------------------------------
    #---------------------------------------------------------------

    #USER INPUT DATE -----------------------------------------------
    #---------------------------------------------------------------

    #USER INPUT FOR OUTPUT -----------------------------------------
    #---------------------------------------------------------------

    #USER INPUT FOR AUTOMATE DATA ----------------------------------
    #---------------------------------------------------------------
    #SHOW MESH AND TESTS MESH FUNCTIONS ----------------------------
    def show_mesh(self):
        try :
            meshToShow = tm.load(self.mesh)
            meshToShow.show()
        except IOError:
            self.popupmsg("Error : Mesh file not found !")
        
    #---------------------------------------------------------------


    #START SIMULATION ----------------------------------------------
    def start_simulation(self):
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

        if(self.timestep == ""):
            self.popupmsg("you need to enter a timestep value !")

        if(self.mesh == ""): #add error catch on file not found
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



