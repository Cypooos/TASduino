import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def alert():
  messagebox.showinfo("Hey !\nI am yet to be created.")

class GraphicalUserInterface():

  def __init__(self,tasManager,compiler):
    self.windows = tk.Tk()
    self.tasManager = tasManager
    self.compiler = compiler
  
  def openTAS(self):
    filepath = filedialog.askopenfilename(title="Ouvrir une TAS",filetypes=[('TAS absolute format','.tas'),('TAS relative format','.rtas'),('all files','.*')])
    self.tasManager.openTAS(filepath)
    alert()
    return
  
  def setupMenu(self):

    menubar = tk.Menu(self.windows)

    menu_file = tk.Menu(menubar, tearoff=0)
    menu_file.add_command(label="Create", command=alert)
    menu_file.add_command(label="Open", command=alert)
    menu_file.add_separator()
    menu_file.add_command(label="Quit", command=self.windows.quit)
    menubar.add_cascade(label="File", menu=menu_file)


    menu_compiler = tk.Menu(menubar, tearoff=0)
    menu_compiler.add_command(label="Compile", command=self.compiler.compileProgram)
    menu_compiler.add_command(label="Assemble", command=self.compiler.assembleProgram)
    menu_compiler.add_command(label="Send", command=self.compiler.sendProgram)
    
    menu_compiler_models = tk.Menu(menubar, tearoff=0)
    def setFirm(firm):
      self.compiler.options["dfu-model"] = firm
    for x in self.compiler.options["Valid Firmwares"]:
      menu_compiler_models.add_radiobutton(label=x, command=lambda:setFirm(x))
    menu_compiler_models.add_separator()
    menu_compiler_models.add_command(label="Quitter", command=self.windows.quit)

    menu_compiler.add_cascade(label="Select dfu",menu=menu_compiler_models)
    menubar.add_cascade(label="Compiler", menu=menu_compiler)

    self.windows.config(menu=menubar)

  def start(self):
    self.setupMenu()
    #Tkinter.Tk.report_callback_exception = show_error
    self.windows.mainloop()
    