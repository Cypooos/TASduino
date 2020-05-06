import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def alert():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be created.")
def link():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be linked.")

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
    menu_file.add_command(label="Create", command=link)
    menu_file.add_command(label="Open", command=link)
    menu_file.add_command(label="Save", command=link)
    menu_file.add_command(label="Save as", command=link)
    menu_file.add_separator()
    menu_file.add_command(label="Convert", command=link) # cascade
    menu_file.add_command(label="Quit", command=self.windows.quit)
    menubar.add_cascade(label="File", menu=menu_file)


    menu_compiler = tk.Menu(menubar, tearoff=0)
    menu_compiler.add_command(label="Assemble", command=self.compiler.assembleProgram)
    menu_compiler.add_command(label="Compile", command=self.compiler.compileJoystick)
    
    menu_compiler_models = tk.Menu(menubar, tearoff=0)
    def setFirm(firm):
      self.compiler.options["dfu-model"] = firm
    for x in self.compiler.options["Basic Firmwares"]:
      menu_compiler_models.add_radiobutton(label=x, command=lambda:setFirm(x))
    menu_compiler_models.add_separator()
    menu_compiler_models.add_command(label="Reload", command=lambda : self.compiler.reloadBasicFirmwares)
    menu_compiler_models.add_command(label="Reset Firmware", command=lambda : self.compiler.resetFirmware())
    menu_compiler.add_cascade(label="Set dfu model",menu=menu_compiler_models)

    menu_compiler_send = tk.Menu(menubar, tearoff=0)
    def sendFirm(firm):
      self.compiler.sendFirmware(firm)
    for x in self.compiler.options["Firmwares"]:
      menu_compiler_send.add_radiobutton(label=x, command=lambda:sendFirm(x))
    menu_compiler_send.add_separator()
    menu_compiler_send.add_command(label="Reload", command=lambda : self.compiler.reloadFirmwares())
    menu_compiler.add_cascade(label="Send Firmware",menu=menu_compiler_send)
    
    menu_compiler_joystick = tk.Menu(menubar, tearoff=0)
    def setJoy(joy):
      self.tasManager.activeTas.metadata["joystick"] = joy # put in metadata of TAS file the joy connected
    for x in self.compiler.options["Joysticks"]:
      menu_compiler_joystick.add_radiobutton(label=x, command=lambda:setJoy(x))
    menu_compiler_joystick.add_separator()
    menu_compiler_joystick.add_command(label="Reload", command=lambda : self.compiler.reloadJoysticks())
    menu_compiler.add_cascade(label="Joysticks",menu=menu_compiler_joystick)

    menubar.add_cascade(label="Compiler", menu=menu_compiler)


    menu_info = tk.Menu(menubar, tearoff=0)
    menu_info.add_command(label="Informations", command=lambda : messagebox.showinfo("Informations","Go to the GitHub for more information about the project !\nhttps://github.com/Discursif/TASduino"))
    menu_info.add_command(label="Credits", command=lambda : messagebox.showinfo("Credits","TASduino is created by </Discursif>\nWith the help of the TASbot discord\nThanks to MonsterDruide1#7702 for his Joystick's script <3"))
    menu_info.add_command(label="Help", command=lambda : messagebox.showinfo("Help","TASduino have a wiki !\nhttps://github.com/Discursif/TASduino/wiki"))
    menubar.add_cascade(label="More", menu=menu_info)

    self.windows.config(menu=menubar)

  def start(self):
    self.setupMenu()
    #Tkinter.Tk.report_callback_exception = show_error
    self.windows.mainloop()
    