from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import simulation


class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("InExES")
        self.minsize(640,400)
        #self.wm_iconbitmap('blabla.ico') get an icon 
        self.labelFrame = ttk.LabelFrame(self, text = "Open a file")
        self.labelFrame.grid(column = 0, row = 2)
        self.mesh = ""

        self.load_mesh()

    def load_mesh(self):
        self.btnMeshLoad = ttk.Button(self.labelFrame, text="browse a file", command = self.fileDialog)
        self.btnMeshLoad.grid(column = 1, row = 2)

    def fileDialog(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title = "select a mesh")
        self.meshName = ttk.Label(self.labelFrame, text = "")
        self.meshName.grid(column = 2, row = 2)
        self.meshName.configure(text = self.fileName)
        self.mesh = self.fileName
