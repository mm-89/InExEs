from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import simulation
from datetime import datetime as dt


class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("InExES")
        self.minsize(640,400)
        #self.wm_iconbitmap('blabla.ico') get an icon 

        # WIDGET CREATION ------------------------------------------
        self.labelFrame = ttk.LabelFrame(self, text = "Open a file")
        self.labelFrame.grid(column = 0, row = 2)
        # ----------------------------------------------------------

        # FRAMES ---------------------------------------------------
        # ----------------------------------------------------------

        #NECESSARY PARAMETERS FOR SIMULATION -----------------------
        self.startDate = ""
        self.endDate = ""
        self.timestep = ""
        self.mesh = ""
        self.outputName = ""
        self.latitude = ""
        self.readData = True
        self.dataPath = ""
        #-----------------------------------------------------------

        # SHOW WIDGET INTO THE MAIN WINDOW -------------------------
        self.load_mesh()
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

    #TESTS AND ERRORS USER -----------------------------------------
    def popupmsg(self,msg):
        popup = self.Tk()
        popup.wm_title("Error found !")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()


    def error_catch(self):
        start = dt.strptime(self.startDate,"%b %d %Y %H:%M:%S")
        end = dt.strptime(self.endDate,"%b %d %Y %H:%M:%S")
        if(start > end) :
            self.popupmsg("start date is posterior to end date !")

        if(self.timestep == ""):
            self.popupmsg("you need to enter a timestep value !")

        if(self.mesh == ""): #add error catch on file not found
            self.popupmsg("Mesh not found")

        if(self.outputName == ""):
            self.popupmsg("you need to enter a output name !")

        if(self.readData == True and self.dataPath == ""): #add error catch on file not found
            self.popupmsg("You choose to use a data file, but no file found !")

        if(self.readData == False and self.latitude == ""): #add error catch on file not found
            self.popupmsg("You choose to generate data automatically, but no latitude value found !")


